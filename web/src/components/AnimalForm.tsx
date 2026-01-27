import { useForm } from 'react-hook-form'
import type { CreateAnimalData, Animal } from '../api/animals'

interface AnimalFormProps {
    animal?: Animal
    onSubmit: (data: CreateAnimalData) => void
    isSubmitting: boolean
    onCancel: () => void
}

export default function AnimalForm({ animal, onSubmit, isSubmitting, onCancel }: AnimalFormProps) {
    const { register, handleSubmit, formState: { errors } } = useForm<CreateAnimalData>({
        defaultValues: animal
    })

    const handleFormSubmit = (data: CreateAnimalData) => {
        // Convert empty strings to null values
        const cleanedData = Object.fromEntries(
            Object.entries(data).map(([key, value]) => [
                key,
                value === '' ? null : value
            ])
        ) as CreateAnimalData

        onSubmit(cleanedData)
    }

    return (
        <form onSubmit={handleSubmit(handleFormSubmit)} className="space-y-4 p-6 rounded shadow">
            <div>
                <label className="block font-medium mb-1">
                    Name<span className='text-red-400'>*</span>
                </label>
                <input
                    {...register('name', { 
                        required: 'Name is required', 
                        minLength: { value: 2, message: 'Name must be at least 2 characters'},
                        maxLength: { value: 50, message: 'Name must be less than 50 characters'}
                    })}
                    placeholder='Roza, Pablo, Sonia, Timos, etc'
                    className="w-full border rounded px-3 py-2"
                />
                {errors.name && <p className="text-red-400 text-sm pt-1">{errors.name.message}</p>}
            </div>

            <div>
                <label className="block font-medium mb-1">
                    Species<span className='text-red-400'>*</span>
                </label>
                <select
                    {...register('species', { required: 'Species is required' })}
                    className="w-full border rounded px-3 py-2"
                >
                    <option value="">Select...</option>
                    <option value="dog">Dog</option>
                    <option value="cat">Cat</option>
                    <option value="other">Other</option>
                </select>
                {errors.species && <p className="text-red-400 text-sm pt-1">{errors.species.message}</p>}
            </div>

            <div>
                <label className="block font-medium mb-1">Breed</label>
                <input
                    {...register('breed')}
                    placeholder='German Shepherd, Kokoni, mix, etc'
                    className="w-full border rounded px-3 py-2"
                />
            </div>

            <div className="grid grid-cols-2 gap-4">
                <div>
                    <label className="block font-medium mb-1">
                        Age<span className='text-red-400'>*</span>
                    </label>
                    <input
                        {...register('age', { 
                            required: 'Age is required', 
                            min: { value: 1, message: 'Age must be greater than zero'}, 
                            max: { value: 100, message: 'Age must be less or equal than 100'} 
                        })}
                        placeholder='Age'
                        className="w-full border rounded px-3 py-2"
                    />
                    {errors.age && <p className="text-red-400 text-sm pt-1">{errors.age.message}</p>}
                </div>

                <div>
                    <label className="block font-medium mb-1">
                        Age Unit<span className='text-red-400'>*</span>
                    </label>
                    <select
                        {...register('age_unit', { required: true })}
                        className="w-full border rounded px-3 py-2"
                    >
                        <option value="">Select...</option>
                        <option value="months">Months</option>
                        <option value="years">Years</option>
                    </select>
                </div>
            </div>

            <div>
                <label className="block font-medium mb-1">
                    Gender<span className='text-red-400'>*</span>
                </label>
                <select
                    {...register('gender', { required: 'Gender is required' })}
                    className="w-full border rounded px-3 py-2"
                >
                    <option value="">Select...</option>
                    <option value="male">Male</option>
                    <option value="female">Female</option>
                </select>
                {errors.gender && <p className="text-red-400 text-sm pt-1">{errors.gender.message}</p>}
            </div>

            <div>
                <label className="block font-medium mb-1">Size</label>
                <select
                    {...register('size')}
                    className="w-full border rounded px-3 py-2"
                >
                    <option value="">Select size...</option>
                    <option value="small">Small</option>
                    <option value="medium">Medium</option>
                    <option value="large">Large</option>
                </select>
            </div>

            {/* <div>
                <label className="block font-medium mb-1">Current Location</label>
                <select
                    {...register('current_location')}
                    className="w-full border rounded px-3 py-2"
                >
                    <option value="">Select current location...</option>
                    <option value="stray">Stray</option>
                    <option value="shelter">Shelter</option>
                    <option value="fostered">Fostered</option>
                </select>
            </div>

            <div>
                <label className="block font-medium mb-1">Adoption Status</label>
                <select
                    {...register('adoption_status')}
                    className="w-full border rounded px-3 py-2"
                >
                    <option value="available">Available</option>
                    <option value="adopted">Adopted</option>
                    <option value="adopted">On hold</option>
                </select>
            </div> */}

            <div>
                <label className="block font-medium mb-1">Description</label>
                <textarea
                    {...register('description')}
                    rows={4}
                    placeholder='A brief description of your animal...'
                    className="w-full border rounded px-3 py-2"
                />
            </div>

            <div>
                <label className="block font-medium mb-1">Medical Notes</label>
                <textarea
                    {...register('medical_notes')}
                    rows={3}
                    placeholder="Any information on the animal's medical history..."
                    className="w-full border rounded px-3 py-2"
                />
            </div>

            <div>
                <label className="block font-medium mb-1">Behavioral Notes</label>
                <textarea
                    {...register('behavioral_notes')}
                    rows={3}
                    placeholder="Any information on the animal's behavior..."
                    className="w-full border rounded px-3 py-2"
                />
            </div>

            <div className="flex space-x-4 pt-4">
                <button
                    type="submit"
                    disabled={isSubmitting}
                    className="bg-blue-600 font-semibold text-white px-6 py-2 rounded cursor-pointer hover:bg-blue-700 disabled:bg-gray-400"
                >
                    {isSubmitting ? 'Saving...' : 'Save'}
                </button>
                <button
                    type="button"
                    onClick={onCancel}
                    className="px-6 py-2 rounded cursor-pointer hover:underline"
                >
                    Cancel
                </button>
            </div>
        </form>
    )
}