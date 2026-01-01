'use client'

import { useState, useEffect } from 'react'
import { api } from '@/lib/api'
import toast from 'react-hot-toast'
import Link from 'next/link'
import { EyeIcon, ChartBarIcon, TrashIcon } from '@heroicons/react/24/outline'

interface Timetable {
  id: number
  timetable_name: string
  fitness: number
  created_at: string
  fitness_progression?: number[]
}

export default function TimetablesPage() {
  const [timetables, setTimetables] = useState<Timetable[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchTimetables()
  }, [])

  const fetchTimetables = async () => {
    setLoading(true)
    try {
      const response = await api.get('/timetables/')
      const data = response.data
      const results = Array.isArray(data) ? data : data.results || []
      setTimetables(results)
    } catch (error) {
      toast.error('Failed to fetch timetables')
    } finally {
      setLoading(false)
    }
  }

  const deleteTimetable = async (id: number) => {
    if (!confirm('Are you sure you want to delete this timetable?')) return

    try {
      await api.delete(`/timetables/${id}/`)
      toast.success('Timetable deleted successfully')
      fetchTimetables()
    } catch (error) {
      toast.error('Failed to delete timetable')
    }
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
          <h1 className="text-2xl font-bold text-gray-900">Timetables</h1>
          <p className="text-gray-600">Manage generated timetables</p>
        </div>
        <Link href="/dashboard/timetables/generate" className="btn-primary">
          Generate New Timetable
        </Link>
      </div>

      <div className="card">
        <div className="overflow-x-auto">
          <table className="min-w-full">
            <thead>
              <tr className="table-header">
                <th className="px-6 py-3 text-left">Name</th>
                <th className="px-6 py-3 text-left">Fitness Score</th>
                <th className="px-6 py-3 text-left">Created</th>
                <th className="px-6 py-3 text-left">Actions</th>
              </tr>
            </thead>
            <tbody>
              {timetables.map((timetable) => (
                <tr key={timetable.id} className="hover:bg-gray-50">
                  <td className="table-cell font-medium">{timetable.timetable_name}</td>
                  <td className="table-cell">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                      timetable.fitness >= 90 ? 'bg-green-100 text-green-800' :
                      timetable.fitness >= 70 ? 'bg-yellow-100 text-yellow-800' :
                      'bg-red-100 text-red-800'
                    }`}>
                      {timetable.fitness?.toFixed(1)}%
                    </span>
                  </td>
                  <td className="table-cell text-gray-600">
                    {new Date(timetable.created_at).toLocaleDateString()}
                  </td>
                  <td className="table-cell">
                    <div className="flex gap-2">
                      <Link
                        href={`/dashboard/timetables/${timetable.id}`}
                        className="text-blue-600 hover:text-blue-900"
                        title="View Timetable"
                      >
                        <EyeIcon className="h-4 w-4" />
                      </Link>
                      {timetable.fitness_progression && timetable.fitness_progression.length > 0 && (
                        <Link
                          href={`/dashboard/timetables/${timetable.id}/fitness-progression`}
                          className="text-purple-600 hover:text-purple-900"
                          title="View Fitness Progression"
                        >
                          <ChartBarIcon className="h-4 w-4" />
                        </Link>
                      )}
                      <button
                        onClick={() => deleteTimetable(timetable.id)}
                        className="text-red-600 hover:text-red-900"
                        title="Delete Timetable"
                      >
                        <TrashIcon className="h-4 w-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>

          {timetables.length === 0 && (
            <div className="text-center py-8 text-gray-500">
              No timetables found. Generate your first timetable to get started.
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
