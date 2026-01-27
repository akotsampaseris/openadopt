import { useQuery } from '@tanstack/react-query'
import { useParams, Link } from 'react-router-dom'
import { useState } from 'react'
import DeleteAnimalModal from '../../components/DeleteAnimalModal'
import { useAuth } from '../../context/AuthContext'
import { getAnimal } from '../../api/animals'

export default function AnimalDetailsPage() {
    const { id } = useParams()
    const { accessToken } = useAuth()
    const [deleteModal, setDeleteModal] = useState<{ id: number, name: string} | null>(null)


    const { data: animal, isLoading, error } = useQuery({
        queryKey: ['animal', id],
        queryFn: () => getAnimal(accessToken!, Number(id)),
        enabled: !!accessToken && !!id
    })

    if (isLoading) return <div className="p-8">Loading...</div>
    if (error) return <div className="p-8 text-red-600">Error loading animal</div>
    if (!animal) return <div className="p-8">Animal not found</div>

    return (
        <>
        <div className="p-8 max-w-3xl mx-auto">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold">{animal.name}</h1>
                <div className="space-x-2">
                    <Link
                        to={`/admin/animals/${animal.id}/edit`}
                        className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
                    >
                        Edit {animal.name}
                    </Link>
                    <Link
                        to="/admin/animals"
                        className="px-4 py-2 rounded hover:underline"
                    >
                        Back to List
                    </Link>
                </div>
            </div>

            <div className="rounded-lg shadow p-6 space-y-4">
                {!animal.primary_photo_url && (
                    <div className='w-100 h-100 bg-white rounded'>
                        <img
                            src={animal.primary_photo_url}
                            alt={animal.name}
                            className="w-full h-64 object-cover rounded"
                        />
                    </div>
                )}

                <div className="grid grid-cols-2 gap-4">
                    <div>
                        <label className="font-semibold">Species:</label>
                        <p>{animal.species}</p>
                    </div>
                    <div>
                        <label className="font-semibold">Breed:</label>
                        <p>{animal.breed || 'N/A'}</p>
                    </div>
                    <div>
                        <label className="font-semibold">Age:</label>
                        <p>{animal.age} {animal.age_unit}</p>
                    </div>
                    <div>
                        <label className="font-semibold">Gender:</label>
                        <p>{animal.gender}</p>
                    </div>
                    <div>
                        <label className="font-semibold">Size:</label>
                        <p>{animal.size || 'N/A'}</p>
                    </div>
                    <div>
                        <label className="font-semibold">Status:</label>
                        <p className="capitalize">{animal.adoption_status}</p>
                    </div>
                    {animal.current_location && (
                        <div>
                            <label className="font-semibold">Current Location:</label>
                            <p>{animal.current_location}</p>
                        </div>
                    )}
                </div>

                {animal.description && (
                    <div>
                        <label className="font-semibold">Description:</label>
                        <p className="whitespace-pre-line">{animal.description}</p>
                    </div>
                )}

                {animal.medical_notes && (
                    <div>
                        <label className="font-semibold">Medical Notes:</label>
                        <p className="whitespace-pre-line">{animal.medical_notes}</p>
                    </div>
                )}

                {animal.behavioral_notes && (
                    <div>
                        <label className="font-semibold">Behavioral Notes:</label>
                        <p className="whitespace-pre-line">{animal.behavioral_notes}</p>
                    </div>
                )}

                <div className="flex justify-between content-start pt-4 border-t text-sm text-gray-400">
                    <div className='flex-wrap'>
                        <div className='flex'>
                            <label className="font-semibold">Created:</label>
                            <p>{new Date(animal.created_at).toLocaleString()}</p>
                        </div>
                        <div className='flex'>
                            <label className="font-semibold">Last Updated:</label>
                            <p>{new Date(animal.updated_at).toLocaleString()}</p>
                        </div>
                    </div>
                    <button
                        onClick={() => setDeleteModal({ id: animal?.id, name: animal?.name})}
                        className="text-red-700 font-semibold rounded cursor-pointer hover:underline">
                        Delete {animal.name}
                    </button>
                </div>
            </div>
        </div>

        {deleteModal && (
            <DeleteAnimalModal
            animalId={deleteModal.id}
            animalName={deleteModal.name}
            onClose={() => setDeleteModal(null)}
            />
        )}
        </>
    )
}