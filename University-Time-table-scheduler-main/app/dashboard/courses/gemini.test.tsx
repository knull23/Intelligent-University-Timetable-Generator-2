import React from 'react'
import { render, screen, waitFor } from '@testing-library/react'
import CoursesPage from './page'
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
]

const departmentList = [
  { id: 1, name: 'Computer Science Engineering', code: 'CSE' },
]

const API_BASE_URL = 'http://localhost:8000/api'

const server = setupServer(
  http.get(`${API_BASE_URL}/courses/`, ({ request }) => {
    return HttpResponse.json({ results: courseList, next: null })
  }),
  http.get(`${API_BASE_URL}/departments/`, () => {
    return HttpResponse.json({ results: departmentList })
  })
)

beforeAll(() => server.listen())
afterEach(() => server.resetHandlers())
afterAll(() => server.close())

describe('CoursesPage', () => {
  test('gemini test: fetches and displays courses', async () => {
    render(<CoursesPage />)

    await waitFor(() => {
      expect(screen.getByText('CS101')).toBeInTheDocument()
    })
  })
})
