import React from 'react'
import { render, screen, waitFor, fireEvent } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import CoursesPage from '../page'
import { http, HttpResponse } from 'msw'
import { setupServer } from 'msw/node'

const courseList = [
  {
    id: 1,
    course_id: 'CS101',
    course_name: 'Intro to CS',
    course_type: 'Theory',
    credits: 3,
    max_students: 50,
    duration: 1,
    classes_per_week: 3,
    year: 1,
    semester: 1,
    department_name: 'Computer Science Engineering'
  },
  {
    id: 3,
    course_id: 'IT102',
    course_name: 'Intermediate IT',
    course_type: 'Theory',
    credits: 3,
    max_students: 40,
    duration: 1,
    classes_per_week: 3,
    year: 1,
    semester: 2,
    department_name: 'Information Technology'
  },
  {
    id: 2,
    course_id: 'DS201',
    course_name: 'Data Structures',
    course_type: 'Theory',
    credits: 4,
    max_students: 45,
    duration: 1,
    classes_per_week: 3,
    year: 2,
    semester: 1,
    department_name: 'Data Science'
  },
  {
    id: 4,
    course_id: 'CS103',
    course_name: 'Advanced CS',
    course_type: 'Theory',
    credits: 3,
    max_students: 35,
    duration: 1,
    classes_per_week: 3,
    year: 1,
    semester: 3,
    department_name: 'Computer Science Engineering'
  }
]

const departmentList = [
  { id: 1, name: 'Computer Science Engineering', code: 'CSE' },
  { id: 2, name: 'Information Technology', code: 'IT' },
  { id: 3, name: 'Data Science', code: 'DS' }
]

const API_BASE_URL = 'http://localhost:8000/api'

const server = setupServer(
  http.get(`${API_BASE_URL}/courses/`, ({ request }) => {
    const url = new URL(request.url)
    const limit = url.searchParams.get('limit')
    return HttpResponse.json({ results: courseList, next: null })
  }),
  http.get(`${API_BASE_URL}/departments/`, () => {
    return HttpResponse.json({ results: departmentList })
  }),
  http.post(`${API_BASE_URL}/courses/`, async ({ request }) => {
    const body = await request.json() as any
    const newCourse = { id: Date.now(), ...body, department_name: departmentList.find(d => d.id === body.department)?.name || 'Unknown' }
    courseList.push(newCourse)
    return HttpResponse.json(newCourse, { status: 201 })
  }),
  http.put(`${API_BASE_URL}/courses/:id/`, async ({ request, params }) => {
    const body = await request.json() as any
    const id = parseInt(params.id as string)
    const index = courseList.findIndex(c => c.id === id)
    if (index !== -1) {
      courseList[index] = { ...courseList[index], ...body }
    }
    return HttpResponse.json(courseList[index], { status: 200 })
  }),
  http.delete(`${API_BASE_URL}/courses/:id/`, ({ params }) => {
    const id = parseInt(params.id as string)
    const index = courseList.findIndex(c => c.id === id)
    if (index !== -1) {
      courseList.splice(index, 1)
    }
    return new HttpResponse(null, { status: 204 })
  }),
  // CORS preflight handlers
  http.options(`${API_BASE_URL}/courses/`, () => {
    return new HttpResponse(null, { status: 200 })
  }),
  http.options(`${API_BASE_URL}/departments/`, () => {
    return new HttpResponse(null, { status: 200 })
  })
)

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

describe('CoursesPage', () => {
  test('fetches and displays courses sorted by department priority then semester', async () => {
    render(<CoursesPage />)

    await waitFor(() => {
      expect(screen.getByText('CS101')).toBeInTheDocument()
      expect(screen.getByText('IT102')).toBeInTheDocument()
      expect(screen.getByText('DS201')).toBeInTheDocument()
      expect(screen.getByText('CS103')).toBeInTheDocument()
    })

    const rows = screen.getAllByRole('row')
    // Header + 4 data rows
    expect(rows).toHaveLength(5)

    // Check sorting by department priority: CSE (1) first, then IT (2), then DS (3)
    // Within CSE, sort by semester: CS101 (sem 1) then CS103 (sem 3)
    const courseIdCells = screen.getAllByText(/CS\d+|IT\d+|DS\d+/)
    const cs101Index = courseIdCells.findIndex(cell => cell.textContent === 'CS101')
    const cs103Index = courseIdCells.findIndex(cell => cell.textContent === 'CS103')
    const it102Index = courseIdCells.findIndex(cell => cell.textContent === 'IT102')
    const ds201Index = courseIdCells.findIndex(cell => cell.textContent === 'DS201')

    // CSE courses should come first
    expect(cs101Index).toBeLessThan(it102Index)
    expect(cs103Index).toBeLessThan(it102Index)
    // IT should come before DS
    expect(it102Index).toBeLessThan(ds201Index)
    // Within CSE, semester 1 before semester 3
    expect(cs101Index).toBeLessThan(cs103Index)
  })

  test('creates a new course with year and semester', async () => {
    render(<CoursesPage />)

    // Wait for departments to load
    await waitFor(() => {
      expect(screen.getByRole('button', { name: /Add Course/i })).toBeInTheDocument()
    })

    // Open modal
    userEvent.click(screen.getByRole('button', { name: /Add Course/i }))

    // Fill form fields
    userEvent.type(screen.getByLabelText(/Course ID/i), 'CS301')
    userEvent.type(screen.getByLabelText(/Course Name/i), 'Algorithms')
    userEvent.selectOptions(screen.getByLabelText(/Course Type/i), ['Theory'])
    userEvent.type(screen.getByLabelText(/Credits/i), '3')
    userEvent.type(screen.getByLabelText(/Max Students/i), '60')
    userEvent.type(screen.getByLabelText(/Duration/i), '1')
    userEvent.type(screen.getByLabelText(/Classes per Week/i), '3')
    userEvent.selectOptions(screen.getByLabelText(/Department/i), ['1'])
    userEvent.selectOptions(screen.getByLabelText(/Year/i), ['3'])
    userEvent.selectOptions(screen.getByLabelText(/Semester/i), ['2'])

    // Submit form
    userEvent.click(screen.getByRole('button', { name: /Create Course/i }))

    await waitFor(() => {
      expect(screen.getByText('CS301')).toBeInTheDocument()
    })
  })

  test('edits a course year and semester', async () => {
    render(<CoursesPage />)

    await waitFor(() => screen.getByText('CS101'))

    // Click edit for first course
    userEvent.click(screen.getAllByRole('button', { name: /Edit/i })[0])

    // Change year and semester
    userEvent.selectOptions(screen.getByLabelText(/Year/i), ['4'])
    userEvent.selectOptions(screen.getByLabelText(/Semester/i), ['3'])

    // Submit update
    userEvent.click(screen.getByRole('button', { name: /Update Course/i }))

    await waitFor(() => {
      expect(screen.getAllByText('4')[0]).toBeInTheDocument()
      expect(screen.getAllByText('3')[0]).toBeInTheDocument()
    })
  })

  test('deletes a course', async () => {
    global.confirm = jest.fn(() => true) // Mock confirm dialog to 'OK'
    render(<CoursesPage />)

    await waitFor(() => screen.getByText('CS101'))

    // Click delete for first course
    userEvent.click(screen.getAllByRole('button', { name: /Delete/i })[0])

    await waitFor(() => {
      expect(screen.queryByText('CS101')).not.toBeInTheDocument()
    })
  })
})
