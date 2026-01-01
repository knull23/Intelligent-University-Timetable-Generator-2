'use client'

import { useState, useEffect } from 'react'
import { api } from '@/lib/api'
import { useForm } from 'react-hook-form'
import { useRouter } from 'next/navigation'
import toast from 'react-hot-toast'
import {
  SparklesIcon,
  AdjustmentsHorizontalIcon,
  InformationCircleIcon
} from '@heroicons/react/24/outline'

interface Department {
  id: number
  name: string
  code: string
}

interface GenerateForm {
  department_ids: number[]
  years: number[]
  semester: string | number
  population_size: number
  mutation_rate: number
  elite_rate: number
  generations: number
}

export default function GenerateTimetablePage() {
  const [departments, setDepartments] = useState<Department[]>([])
  const [loading, setLoading] = useState(false)
  const [showAdvanced, setShowAdvanced] = useState(false)
  const router = useRouter()

  const { register, handleSubmit, setValue, watch, formState: { errors } } = useForm<GenerateForm>({
    defaultValues: {
      department_ids: [],
      years: [],
      semester: 'odd',
      population_size: 100,
      mutation_rate: 0.1,
      elite_rate: 0.1,
      generations: 1000,
    }
  })

  const watchedDepartments = watch('department_ids')
  const watchedYears = watch('years')

  const years = [
    { value: 1, label: '1st Year' },
    { value: 2, label: '2nd Year' },
    { value: 3, label: '3rd Year' },
    { value: 4, label: '4th Year' },
  ]

  const semesters = [
    { value: 'odd', label: 'Odd Semesters (1, 3, ...)' },
    { value: 'even', label: 'Even Semesters (2, 4, ...)' },
  ]

  useEffect(() => {
    fetchDepartments()
  }, [])

  const fetchDepartments = async () => {
    try {
      const response = await api.get('/departments/')
      setDepartments(response.data.results || response.data)
    } catch (error) {
      toast.error('Failed to fetch departments')
    }
  }

  const handleDepartmentChange = (deptId: number, checked: boolean) => {
    const currentDepartments = watchedDepartments || []
    if (checked) {
      setValue('department_ids', [...currentDepartments, deptId])
    } else {
      setValue('department_ids', currentDepartments.filter(id => id !== deptId))
    }
  }

  const handleYearChange = (year: number, checked: boolean) => {
    const currentYears = watchedYears || []
    if (checked) {
      setValue('years', [...currentYears, year])
    } else {
      setValue('years', currentYears.filter(y => y !== year))
    }
  }

  const onSubmit = async (data: GenerateForm) => {
    if (!data.department_ids?.length || !data.years?.length) {
      toast.error('Please select at least one department and one year')
      return
    }

    setLoading(true)

    try {
      const response = await api.post('/timetables/generate/', data)
      const timetableId = response.data.timetable_id
      const fitness = response.data.fitness

      toast.success(
        `Timetable generated successfully (Fitness: ${fitness?.toFixed?.(1) ?? fitness}%)`
      )

      if (timetableId) {
        router.push(`/dashboard/timetables/${timetableId}`)
      } else {
        router.push('/dashboard/timetables')
      }
    } catch (error: any) {
      toast.error(error.response?.data?.error || 'Failed to generate timetables')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-2xl mx-auto space-y-6 animate-fade-in">
      <div className="text-center">
        <div className="mx-auto h-16 w-16 bg-gradient-to-br from-gray-900 to-gray-700 rounded-full flex items-center justify-center mb-4">
          <SparklesIcon className="h-8 w-8 text-white" />
        </div>
        <h1 className="text-2xl font-bold text-gray-900 mb-2">Generate Timetable</h1>
        <p className="text-gray-600">
          Create an optimized timetable using advanced genetic algorithms
        </p>
      </div>

      <div className="card p-6">
        <form onSubmit={handleSubmit(onSubmit)} className="space-y-6">
          {/* Department Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-3">
              Select Departments
            </label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {departments.map(dept => (
                <label key={dept.id} className="flex items-center space-x-3 p-3 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={watchedDepartments?.includes(dept.id) || false}
                    onChange={(e) => handleDepartmentChange(dept.id, e.target.checked)}
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  />
                  <div>
                    <div className="font-medium text-gray-900">{dept.name}</div>
                    <div className="text-sm text-gray-500">{dept.code}</div>
                  </div>
                </label>
              ))}
            </div>
            {errors.department_ids && (
              <p className="text-red-600 text-sm mt-1">At least one department is required</p>
            )}
          </div>

          {/* Year Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-3">
              Select Years
            </label>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
              {years.map(year => (
                <label key={year.value} className="flex items-center space-x-3 p-3 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={watchedYears?.includes(year.value) || false}
                    onChange={(e) => handleYearChange(year.value, e.target.checked)}
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                  />
                  <span className="text-gray-900">{year.label}</span>
                </label>
              ))}
            </div>
            {errors.years && (
              <p className="text-red-600 text-sm mt-1">At least one year is required</p>
            )}
          </div>

          {/* Semester Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-3">
              Select Semester Type
            </label>
            <div className="grid grid-cols-2 gap-3">
              {semesters.map(semester => (
                <label key={semester.value} className="flex items-center space-x-3 p-3 border border-gray-200 rounded-lg hover:bg-gray-50 cursor-pointer">
                  <input
                    type="radio"
                    value={semester.value}
                    {...register('semester')}
                    className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300"
                  />
                  <span className="text-gray-900">{semester.label}</span>
                </label>
              ))}
            </div>
          </div>

          <div className="border-t pt-6">
            <button
              type="button"
              onClick={() => setShowAdvanced(!showAdvanced)}
              className="flex items-center text-sm text-gray-600 hover:text-gray-900 mb-4"
            >
              <AdjustmentsHorizontalIcon className="h-4 w-4 mr-2" />
              Advanced Algorithm Settings
              <span className="ml-2 text-xs">
                {showAdvanced ? '(Hide)' : '(Show)'}
              </span>
            </button>

            {showAdvanced && (
              <div className="space-y-4 p-4 bg-gray-50 rounded-lg">
                <div className="flex items-start gap-3 text-sm text-gray-600 mb-4">
                  <InformationCircleIcon className="h-5 w-5 text-blue-500 flex-shrink-0 mt-0.5" />
                  <p>
                    These settings control the genetic algorithm parameters.
                    Default values work well for most cases.
                  </p>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Population Size
                    </label>
                    <input
                      {...register('population_size', {
                        min: { value: 10, message: 'Minimum 10' },
                        max: { value: 200, message: 'Maximum 200' }
                      })}
                      type="number"
                      className="input-field"
                      placeholder="100"
                    />
                    <p className="text-xs text-gray-500 mt-1">Number of candidate solutions per generation</p>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Generations
                    </label>
                    <input
                      {...register('generations', {
                        min: { value: 50, message: 'Minimum 50' },
                        max: { value: 2000, message: 'Maximum 2000' }
                      })}
                      type="number"
                      className="input-field"
                      placeholder="1000"
                    />
                    <p className="text-xs text-gray-500 mt-1">Maximum number of evolution cycles</p>
                  </div>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Mutation Rate
                    </label>
                    <input
                      {...register('mutation_rate', {
                        min: { value: 0.01, message: 'Minimum 0.01' },
                        max: { value: 0.5, message: 'Maximum 0.5' }
                      })}
                      type="number"
                      step="0.01"
                      className="input-field"
                      placeholder="0.1"
                    />
                    <p className="text-xs text-gray-500 mt-1">Probability of random changes (0.01-0.5)</p>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      Elite Rate
                    </label>
                    <input
                      {...register('elite_rate', {
                        min: { value: 0.05, message: 'Minimum 0.05' },
                        max: { value: 0.3, message: 'Maximum 0.3' }
                      })}
                      type="number"
                      step="0.01"
                      className="input-field"
                      placeholder="0.1"
                    />
                    <p className="text-xs text-gray-500 mt-1">Portion of best solutions to preserve (0.05-0.3)</p>
                  </div>
                </div>
              </div>
            )}
          </div>

          <div className="flex gap-4">
            <button
              type="submit"
              disabled={loading}
              className="btn-primary flex-1 flex items-center justify-center gap-2 py-3"
            >
              {loading ? (
                <>
                  <div className="loading-spinner" />
                  Generating...
                </>
              ) : (
                <>
                  <SparklesIcon className="h-5 w-5" />
                  Generate Timetable
                </>
              )}
            </button>
            <button
              type="button"
              onClick={() => router.back()}
              className="btn-secondary px-6"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>

      <div className="card p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-3">How it works</h3>
        <div className="space-y-3 text-sm text-gray-600">
          <div className="flex items-start gap-3">
            <div className="w-6 h-6 bg-gray-900 text-white rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0">
              1
            </div>
            <p>
              The algorithm creates multiple random timetable configurations
            </p>
          </div>
          <div className="flex items-start gap-3">
            <div className="w-6 h-6 bg-gray-900 text-white rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0">
              2
            </div>
            <p>
              Each configuration is evaluated for conflicts (instructor, room, student clashes)
            </p>
          </div>
          <div className="flex items-start gap-3">
            <div className="w-6 h-6 bg-gray-900 text-white rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0">
              3
            </div>
            <p>
              The best configurations are selected and combined to create improved solutions
            </p>
          </div>
          <div className="flex items-start gap-3">
            <div className="w-6 h-6 bg-gray-900 text-white rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0">
              4
            </div>
            <p>
              This process repeats until an optimal conflict-free timetable is found
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
