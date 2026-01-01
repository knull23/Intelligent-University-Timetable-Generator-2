'use client'

import { useState, useEffect } from 'react'
import { api } from '@/lib/api'
import { useParams } from 'next/navigation'
import toast from 'react-hot-toast'
import FitnessProgressionChart from '@/components/FitnessProgressionChart'
import { ArrowLeftIcon } from '@heroicons/react/24/outline'
import Link from 'next/link'

interface TimetableData {
  timetable_name: string
  fitness: number
  fitness_progression: number[]
}

export default function FitnessProgressionPage() {
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
      const response = await api.get(`/timetables/${params.id}/`)
      setTimetable(response.data)
    } catch (error) {
      toast.error('Failed to fetch timetable details')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div className="h-8 bg-gray-200 rounded w-64 animate-pulse"></div>
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
      <div className="flex items-center gap-4">
        <Link
          href={`/dashboard/timetables/${params.id}`}
          className="text-gray-400 hover:text-gray-600"
        >
          <ArrowLeftIcon className="h-6 w-6" />
        </Link>
        <div>
          <h1 className="text-2xl font-bold text-gray-900">
            Fitness Progression - {timetable.timetable_name}
          </h1>
          <p className="text-sm text-gray-600 mt-1">
            Final Fitness Score: {timetable.fitness?.toFixed(1)}%
          </p>
        </div>
      </div>

      {timetable.fitness_progression && timetable.fitness_progression.length > 0 ? (
        <FitnessProgressionChart
          data={timetable.fitness_progression}
          title={`Fitness Progression Over ${timetable.fitness_progression.length} Generations`}
        />
      ) : (
        <div className="card p-12 text-center">
          <h3 className="text-lg font-medium text-gray-900 mb-2">No Fitness Progression Data</h3>
          <p className="text-gray-600 mb-6">
            This timetable was generated before fitness progression tracking was implemented.
          </p>
          <Link href={`/dashboard/timetables/${params.id}`} className="btn-primary">
            Back to Timetable
          </Link>
        </div>
      )}
    </div>
  )
}
