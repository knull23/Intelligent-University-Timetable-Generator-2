'use client'

import { useState, useEffect } from 'react'
import { api } from '@/lib/api'
import { useParams } from 'next/navigation'
import toast from 'react-hot-toast'
import TimetableGrid from '@/components/TimetableGrid'
import { ArrowLeftIcon, ChartBarIcon, DocumentArrowDownIcon } from '@heroicons/react/24/outline'
import Link from 'next/link'

interface SectionData {
  section_id: string
  section_name: string
  schedule: Record<string, Record<string, any[]>>
  courses: any[]
  instructors: any[]
}

interface TimetableData {
  id: number
  timetable_name: string
  fitness: number
  created_at: string
  fitness_progression?: number[]
  sections: SectionData[]
}

export default function TimetableViewPage() {
  const [timetable, setTimetable] = useState<TimetableData | null>(null)
  const [loading, setLoading] = useState(true)
  const params = useParams()

  useEffect(() => {
    if (params.id) {
      fetchTimetable()
    }
  }, [params.id])

  const fetchTimetable = async () => {
    try {
      const response = await api.get(`/timetables/${params.id}/view_schedule/`)
      // Combine schedules from all sections into a single schedule object
      const combinedSchedule: Record<string, Record<string, any>> = {}
      response.data.sections.forEach((section: any) => {
        Object.keys(section.schedule).forEach(day => {
          if (!combinedSchedule[day]) combinedSchedule[day] = {}
          Object.keys(section.schedule[day]).forEach(timeSlot => {
            if (!combinedSchedule[day][timeSlot]) combinedSchedule[day][timeSlot] = []
            combinedSchedule[day][timeSlot].push(...section.schedule[day][timeSlot])
          })
        })
      })
      setTimetable({ ...response.data, schedule: combinedSchedule })
    } catch (error) {
      toast.error('Failed to fetch timetable details')
    } finally {
      setLoading(false)
    }
  }

  const exportTimetable = async () => {
    try {
      const response = await api.get(`/timetables/${params.id}/export/`, {
        responseType: 'blob'
      })
      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', `${timetable?.timetable_name || 'timetable'}.pdf`)
      document.body.appendChild(link)
      link.click()
      link.remove()
      toast.success('Timetable exported successfully')
    } catch (error) {
      toast.error('Failed to export timetable')
    }
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div className="h-8 bg-gray-200 rounded w-64 animate-pulse"></div>
          <div className="h-10 bg-gray-200 rounded w-24 animate-pulse"></div>
        </div>
        <div className="card p-6">
          <div className="h-96 bg-gray-200 rounded animate-pulse"></div>
        </div>
      </div>
    )
  }

  if (!timetable) {
    return (
      <div className="card p-12 text-center">
        <h3 className="text-lg font-medium text-gray-900 mb-2">Timetable not found</h3>
        <p className="text-gray-600 mb-6">
          The requested timetable could not be found or may have been deleted.
        </p>
        <Link href="/dashboard/timetables" className="btn-primary">
          Back to Timetables
        </Link>
      </div>
    )
  }

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-4">
          <Link
            href="/dashboard/timetables"
            className="text-gray-400 hover:text-gray-600"
          >
            <ArrowLeftIcon className="h-6 w-6" />
          </Link>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{timetable.timetable_name}</h1>
            <p className="text-sm text-gray-600 mt-1">
              Fitness Score: {timetable.fitness?.toFixed(1)}% • Created: {new Date(timetable.created_at).toLocaleDateString()}
            </p>
          </div>
        </div>
        <div className="flex gap-2">
          <button
            onClick={exportTimetable}
            className="btn-secondary flex items-center gap-2"
          >
            <DocumentArrowDownIcon className="h-4 w-4" />
            Export PDF
          </button>
          {timetable.fitness_progression && timetable.fitness_progression.length > 0 && (
            <Link
              href={`/dashboard/timetables/${params.id}/fitness-progression`}
              className="btn-secondary flex items-center gap-2"
            >
              <ChartBarIcon className="h-4 w-4" />
              Fitness Progression
            </Link>
          )}
        </div>
      </div>

      <div className="space-y-8">
        {timetable.sections.map((section, index) => (
          <div key={section.section_id} className="space-y-4">
            <div className="border-t pt-6 first:border-t-0 first:pt-0">
              <h2 className="text-xl font-semibold text-gray-900 mb-2">
                {section.section_name}
              </h2>
              <TimetableGrid
                schedule={section.schedule}
                title={`${section.section_name} Schedule`}
                editMode={false}
              />
            </div>

            {/* Instructor Information for this section */}
            {section.instructors && section.instructors.length > 0 && (
              <div className="card overflow-hidden">
                <div className="px-6 py-4 border-b border-gray-200 bg-gray-50">
                  <h3 className="text-lg font-semibold text-gray-900">
                    Instructor Information - {section.section_name}
                  </h3>
                </div>
                <div className="overflow-x-auto">
                  <table className="min-w-full border-collapse">
                    <thead className="bg-gray-50">
                      <tr>
                        <th className="px-2 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b border-r border-gray-200">
                          Instructor
                        </th>
                        <th className="px-2 py-2 text-left text-xs font-medium text-gray-500 uppercase tracking-wider border-b border-gray-200">
                          Courses & Course Codes
                        </th>
                      </tr>
                    </thead>
                    <tbody className="bg-white">
                      {section.instructors.map(instructor => (
                        <tr key={instructor.name} className="border-t border-gray-200">
                          <td className="px-2 py-2 text-xs font-medium text-gray-900 border-r border-gray-200">
                            {instructor.name}
                          </td>
                          <td className="px-2 py-2 text-xs text-gray-700">
                            <div className="space-y-1">
                              {instructor.courses && instructor.courses.map((course: string, idx: number) => (
                                <div key={idx} className="font-semibold">
                                  {course}
                                </div>
                              ))}
                            </div>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
