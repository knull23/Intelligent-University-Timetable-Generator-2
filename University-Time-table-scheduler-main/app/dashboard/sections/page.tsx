'use client'

import React, { useState, useEffect } from 'react'
import { api } from '@/lib/api'
import { useForm, useWatch } from 'react-hook-form'
import toast from 'react-hot-toast'
import Modal from '@/components/Modal'
import { PlusIcon, PencilIcon, TrashIcon } from '@heroicons/react/24/outline'

interface Section {
  id?: number
  section_id: string
  department: number
  year: number
  semester: number
  num_students: number
  instructors?: number[]
  courses?: number[]
  course_instructor_assignments?: {[courseId: string]: number[]}
  department_name?: string
  instructor_names?: string[]
  course_names?: string[]
  courses_detail?: CourseDetail[]
}

interface CourseDetail {
  id: number
  course_id: string
  course_name: string
  instructors: Instructor[]
}

interface Instructor {
  id: number
  name: string
  instructor_id: string
}

const years = [
  { value: 1, label: '1st Year' },
  { value: 2, label: '2nd Year' },
  { value: 3, label: '3rd Year' },
  { value: 4, label: '4th Year' },
]

const semesters = [
  { value: 1, label: 'Semester 1' },
  { value: 2, label: 'Semester 2' },
]

export default function SectionsPage() {
  const [sections, setSections] = useState<Section[]>([])
  const [departments, setDepartments] = useState<any[]>([])
  const [courses, setCourses] = useState<any[]>([])
  const [instructors, setInstructors] = useState<Instructor[]>([])
  const [loading, setLoading] = useState(true)
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [editingSection, setEditingSection] = useState<Section | null>(null)
  const [courseInstructors, setCourseInstructors] = useState<{[courseId: number]: number[]}>({})
  const [currentSemesters, setCurrentSemesters] = useState(semesters)
  const [showInstructorAssignment, setShowInstructorAssignment] = useState(true)



  const { register, handleSubmit, reset, setValue, watch, formState: { errors } } = useForm<Section>()

  const watchedYear = watch('year')
  const watchedCourses = watch('courses')
  const watchedDepartment = watch('department')
  const watchedSemester = watch('semester')

  useEffect(() => {
    fetchSections()
    fetchDepartments()
    fetchCourses()
    fetchInstructors()
  }, [])



  useEffect(() => {
    if (watchedYear) {
      const year = Number(watchedYear)
      let newSemesters = []
      if (year === 1) {
        newSemesters = [
          { value: 1, label: 'Semester 1' },
          { value: 2, label: 'Semester 2' },
        ]
      } else if (year === 2) {
        newSemesters = [
          { value: 3, label: 'Semester 3' },
          { value: 4, label: 'Semester 4' },
        ]
      } else if (year === 3) {
        newSemesters = [
          { value: 5, label: 'Semester 5' },
          { value: 6, label: 'Semester 6' },
        ]
      } else if (year === 4) {
        newSemesters = [
          { value: 7, label: 'Semester 7' },
          { value: 8, label: 'Semester 8' },
        ]
      }
      setCurrentSemesters(newSemesters)
      // Reset semester if it's not valid for the new year
      if (newSemesters.length > 0 && !newSemesters.some(sem => sem.value === Number(watch('semester')))) {
        setValue('semester', newSemesters[0].value)
      }
    }
  }, [watchedYear, setValue, watch])





  const fetchSections = async () => {
    try {
      const res = await api.get('/sections/')
      // Handle both paginated and non-paginated formats
      const data = Array.isArray(res.data)
        ? res.data
        : res.data.results || []
      setSections(data)
    } catch (err) {
      console.error('❌ Error fetching sections:', err)
      toast.error('Failed to fetch sections')
      setSections([])
    } finally {
      setLoading(false)
    }
  }

  const fetchDepartments = async () => {
    try {
      const res = await api.get('/departments/')
      setDepartments(res.data.results || res.data)
    } catch (err) {
      console.error('❌ Error fetching departments:', err)
    }
  }

  const fetchCourses = async () => {
    try {
      let allCourses: any[] = []
      let nextUrl = '/courses/?limit=100'
      while (nextUrl) {
        const res = await api.get(nextUrl)
        const data = res.data
        const results = data.results || data
        allCourses = allCourses.concat(results)
        nextUrl = data.next || null
      }
      setCourses(allCourses)
    } catch (err) {
      console.error('❌ Error fetching courses:', err)
    }
  }

  const fetchInstructors = async () => {
    try {
      const res = await api.get('/instructors/')
      setInstructors(res.data.results || res.data)
    } catch (err) {
      console.error('❌ Error fetching instructors:', err)
    }
  }



  const onSubmit = async (data: Section) => {
    try {
      // Build course_instructor_assignments from courseInstructors
      const course_instructor_assignments: {[courseId: string]: number[]} = {}
      for (const [courseId, instructorIds] of Object.entries(courseInstructors)) {
        course_instructor_assignments[courseId] = instructorIds
      }
      data.course_instructor_assignments = course_instructor_assignments

      let sectionId: number
      if (editingSection) {
        await api.put(`/sections/${editingSection.id}/`, data)
        sectionId = editingSection.id!
        toast.success('Section updated successfully')
      } else {
        const response = await api.post('/sections/', data)
        sectionId = response.data.id
        toast.success('Section created successfully')
      }

      fetchSections()
      closeModal()
    } catch (error: any) {
      toast.error(error.response?.data?.message || 'Operation failed')
    }
  }

  const deleteSection = async (id: number) => {
    if (!confirm('Are you sure you want to delete this section?')) return

    try {
      await api.delete(`/sections/${id}/`)
      toast.success('Section deleted successfully')
      fetchSections()
    } catch (error) {
      toast.error('Failed to delete section')
    }
  }

  const openModal = async (section?: Section) => {
    if (section) {
      setEditingSection(section)
      Object.keys(section).forEach((key) => {
        setValue(key as keyof Section, section[key as keyof Section])
      })
      // Initialize course instructors from existing data
      const initialCourseInstructors: {[courseId: number]: number[]} = {}
      if (section.courses_detail) {
        section.courses_detail.forEach(course => {
          initialCourseInstructors[course.id] = course.instructors.map(inst => inst.id)
        })
      }
      setCourseInstructors(initialCourseInstructors)
    } else {
      setEditingSection(null)
      // Don't reset form values immediately to avoid filtering issues
      reset({ num_students: 60, instructors: [], courses: [] })
      setCourseInstructors({})
    }
    setIsModalOpen(true)
  }

  const closeModal = () => {
    setIsModalOpen(false)
    setEditingSection(null)
    reset()
  }

  const handleCourseInstructorChange = (courseId: number, instructorId: number, checked: boolean) => {
    setCourseInstructors(prev => ({
      ...prev,
      [courseId]: checked
        ? [...(prev[courseId] || []), instructorId]
        : (prev[courseId] || []).filter(id => id !== instructorId)
    }))
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="flex justify-between items-center">
          <div className="h-8 bg-gray-200 rounded w-48 animate-pulse"></div>
          <div className="h-10 bg-gray-200 rounded w-32 animate-pulse"></div>
        </div>
        <div className="card p-6">
          <div className="space-y-4">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="h-16 bg-gray-200 rounded animate-pulse"></div>
            ))}
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Sections</h1>
          <p className="text-gray-600">Manage student sections and groups</p>
        </div>
        <button
          onClick={() => openModal()}
          className="btn-primary flex items-center gap-2"
        >
          <PlusIcon className="h-5 w-5" />
          Add Section
        </button>
      </div>

      <div className="card">
        <div className="overflow-x-auto">
          <table className="min-w-full">
            <thead>
              <tr className="table-header">
                <th className="px-6 py-3 text-left">Section ID</th>
                <th className="px-6 py-3 text-left">Department</th>
                <th className="px-6 py-3 text-left">Year</th>
                <th className="px-6 py-3 text-left">Semester</th>
                <th className="px-6 py-3 text-left">Students</th>
                <th className="px-6 py-3 text-left">Instructors</th>
                <th className="px-6 py-3 text-left">Actions</th>
              </tr>
            </thead>
            <tbody>
              {sections.map((section) => (
                <tr key={section.id} className="hover:bg-gray-50">
                  <td className="table-cell font-mono">{section.section_id}</td>
                  <td className="table-cell">{section.department_name || 'N/A'}</td>
                  <td className="table-cell">{section.year} Year</td>
                  <td className="table-cell">Semester {section.semester}</td>
                  <td className="table-cell">{section.num_students} students</td>
                  <td className="table-cell">
                    {section.courses_detail && section.courses_detail.length > 0 ? (
                      <div className="text-sm">
                        {Array.from(new Set(
                          section.courses_detail.flatMap(course =>
                            course.instructors.map(inst => inst.name)
                          )
                        )).join(', ')}
                      </div>
                    ) : (
                      <span className="text-gray-400">No instructors assigned</span>
                    )}
                  </td>
                  <td className="table-cell">
                    <div className="flex gap-2">
                      <button
                        onClick={() => openModal(section)}
                        className="text-blue-600 hover:text-blue-900"
                      >
                        <PencilIcon className="h-4 w-4" />
                      </button>
                      <button
                        onClick={() => deleteSection(section.id!)}
                        className="text-red-600 hover:text-red-900"
                      >
                        <TrashIcon className="h-4 w-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {sections.length === 0 && (
            <div className="text-center py-8 text-gray-500">
              No sections found. Add your first section to get started.
            </div>
          )}
        </div>
      </div>

      <Modal
        isOpen={isModalOpen}
        onClose={closeModal}
        title={editingSection ? 'Edit Section' : 'Add New Section'}
      >
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Section ID
            </label>
            <input
              {...register('section_id', { required: 'Section ID is required' })}
              className="input-field"
              placeholder="e.g., CS-A, MECH-B"
            />
            {errors.section_id && (
              <p className="text-red-600 text-sm mt-1">{errors.section_id.message}</p>
            )}
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Department
            </label>
            <select
              {...register('department', { required: 'Department is required' })}
              className="input-field"
            >
              <option value="">Select Department</option>
              {departments.map(dept => (
                <option key={dept.id} value={dept.id}>
                  {dept.name}
                </option>
              ))}
            </select>
            {errors.department && (
              <p className="text-red-600 text-sm mt-1">{errors.department.message}</p>
            )}
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Year
              </label>
              <select
                {...register('year', { required: 'Year is required' })}
                className="input-field"
              >
                {years.map(year => (
                  <option key={year.value} value={year.value}>
                    {year.label}
                  </option>
                ))}
              </select>
              {errors.year && (
                <p className="text-red-600 text-sm mt-1">{errors.year.message}</p>
              )}
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Semester
              </label>
              <select
                {...register('semester', { required: 'Semester is required' })}
                className="input-field"
              >
                {currentSemesters.map(sem => (
                  <option key={sem.value} value={sem.value}>
                    {sem.label}
                  </option>
                ))}
              </select>
              {errors.semester && (
                <p className="text-red-600 text-sm mt-1">{errors.semester.message}</p>
              )}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Courses
            </label>
            <select
              {...register('courses')}
              multiple
              className="input-field"
              size={12}
            >
              {courses.filter(course => {
                if (editingSection) {
                  // When editing, filter by section's department, year, and semester
                  const deptMatch = course.department == editingSection.department
                  const yearMatch = course.year == editingSection.year
                  const semMatch = course.semester == editingSection.semester
                  return deptMatch && yearMatch && semMatch
                } else {
                  // When creating, filter by watched department, year, and semester
                  const deptMatch = !watchedDepartment || course.department == Number(watchedDepartment)
                  const yearMatch = !watchedYear || course.year == Number(watchedYear)
                  const semMatch = !watchedSemester || course.semester == Number(watchedSemester)
                  return deptMatch && yearMatch && semMatch
                }
              }).sort((a, b) => {
                // Sort by semester
                return a.semester - b.semester
              }).map(course => (
                <option key={course.id} value={course.id}>
                  {course.course_id} - {course.course_name}
                </option>
              ))}
            </select>
            <p className="text-xs text-gray-500 mt-1">
              Hold Ctrl/Cmd to select multiple courses.
            </p>

          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Number of Students
            </label>
            <input
              {...register('num_students', {
                required: 'Number of students is required',
                min: { value: 1, message: 'Must have at least 1 student' }
              })}
              type="number"
              className="input-field"
              placeholder="e.g., 60"
            />
            {errors.num_students && (
              <p className="text-red-600 text-sm mt-1">{errors.num_students.message}</p>
            )}
          </div>

          {watchedCourses && watchedCourses.length > 0 && showInstructorAssignment && (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Assign Instructors to Courses
              </label>
              <div className="space-y-4 max-h-96 overflow-y-auto">
                {courses.filter(course => watchedCourses?.map(Number).includes(course.id)).map(course => (
                  <div key={course.id} className="border rounded p-4 bg-gray-50">
                    <h4 className="font-medium text-gray-900 mb-2">
                      {course.course_id} - {course.course_name}
                    </h4>
                    <div>
                      <label className="block text-sm text-gray-600 mb-2">
                        Select Instructors
                      </label>
                      <div className="grid grid-cols-1 gap-2 max-h-80 overflow-y-auto">
                        {instructors.sort((a, b) => a.instructor_id.localeCompare(b.instructor_id)).map((instructor) => (
                          <label key={instructor.id} className="flex items-center space-x-2">
                            <input
                              type="checkbox"
                              checked={(courseInstructors[course.id] || []).includes(instructor.id)}
                              onChange={(e) => handleCourseInstructorChange(course.id, instructor.id, e.target.checked)}
                              className="rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                            />
                            <span className="text-sm">
                              {instructor.name} ({instructor.instructor_id})
                            </span>
                          </label>
                        ))}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}





          <div className="flex gap-3 pt-4">
            <button type="submit" className="btn-primary flex-1">
              {editingSection ? 'Update' : 'Create'} Section
            </button>
            <button
              type="button"
              onClick={closeModal}
              className="btn-secondary flex-1"
            >
              Cancel
            </button>
          </div>
        </form>
      </Modal>


    </div>
  )
}

