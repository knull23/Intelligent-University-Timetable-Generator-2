'use client'

import { useState, useEffect } from 'react'
import { api } from '@/lib/api'
import StatsCard from '@/components/StatsCard'
import { BookOpenIcon, UserGroupIcon, HomeIcon, BuildingOfficeIcon, CalendarDaysIcon } from '@heroicons/react/24/outline'
import Link from 'next/link'

interface Stats {
  courses: number
  instructors: number
  rooms: number
  departments: number
  timetables: number
}

export default function DashboardPage() {
  const [stats, setStats] = useState<Stats>({
    courses: 0,
    instructors: 0,
    rooms: 0,
    departments: 0,
    timetables: 0,
  })
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    setLoading(true)
    try {
      const [coursesRes, instructorsRes, roomsRes, departmentsRes, timetablesRes] = await Promise.all([
        api.get('/courses/'),
        api.get('/instructors/'),
        api.get('/rooms/'),
        api.get('/departments/'),
        api.get('/timetables/'),
      ])

      const getCount = (res: any) => {
        if (Array.isArray(res.data)) return res.data.length
        if (res.data.count !== undefined) return res.data.count
        if (Array.isArray(res.data.results)) return res.data.results.length
        return 0
      }

      setStats({
        courses: getCount(coursesRes),
        instructors: getCount(instructorsRes),
        rooms: getCount(roomsRes),
        departments: getCount(departmentsRes),
        timetables: getCount(timetablesRes),
      })
    } catch (error) {
      console.error('Failed to fetch stats:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="space-y-6">
        <div className="h-8 bg-gray-200 rounded w-48 animate-pulse"></div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-6">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="h-24 bg-gray-200 rounded animate-pulse"></div>
          ))}
        </div>
      </div>
    )
  }

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600">Welcome to the Timetable Management System</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-6">
        <Link href="/dashboard/courses">
          <StatsCard
            title="Courses"
            value={stats.courses}
            icon={BookOpenIcon}
            color="blue"
          />
        </Link>
        <Link href="/dashboard/instructors">
          <StatsCard
            title="Instructors"
            value={stats.instructors}
            icon={UserGroupIcon}
            color="green"
          />
        </Link>
        <Link href="/dashboard/rooms">
          <StatsCard
            title="Rooms"
            value={stats.rooms}
            icon={HomeIcon}
            color="purple"
          />
        </Link>
        <Link href="/dashboard/departments">
          <StatsCard
            title="Departments"
            value={stats.departments}
            icon={BuildingOfficeIcon}
            color="yellow"
          />
        </Link>
        <Link href="/dashboard/timetables">
          <StatsCard
            title="Timetables"
            value={stats.timetables}
            icon={CalendarDaysIcon}
            color="indigo"
          />
        </Link>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h3>
          <div className="space-y-3">
            <Link href="/dashboard/timetables/generate" className="btn-primary w-full text-center block">
              Generate New Timetable
            </Link>
            <Link href="/dashboard/courses" className="btn-secondary w-full text-center block">
              Manage Courses
            </Link>
            <Link href="/dashboard/instructors" className="btn-secondary w-full text-center block">
              Manage Instructors
            </Link>
          </div>
        </div>

        <div className="card p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Activity</h3>
          <p className="text-gray-600">No recent activity to display.</p>
        </div>
      </div>
    </div>
  )
}
