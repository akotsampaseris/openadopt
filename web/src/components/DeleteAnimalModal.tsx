import { useMutation, useQueryClient } from '@tanstack/react-query'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { deleteAnimal } from '../api/animals'

interface DeleteAnimalModalProps {
  animalId: number
  animalName: string
  onClose: () => void
}

export default function DeleteAnimalModal({ animalId, animalName, onClose }: DeleteAnimalModalProps) {
  const { accessToken } = useAuth()
  const queryClient = useQueryClient()
  const navigate = useNavigate()

  const mutation = useMutation({
    mutationFn: () => deleteAnimal(accessToken!, animalId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['animals'] })
      navigate('/admin/animals')
      onClose()
    }
  })

  return (
    <>
    <div className='fixed bg-black opacity-50 inset-0'></div>
    <div className="fixed inset-0 flex items-center justify-center z-50">
      <div className="bg-gray-700 shadow-black shadow-2xl rounded-lg p-6 max-w-2xl w-full mx-4">
        <h2 className="text-xl font-bold mb-4 border-b py-4">Delete Animal</h2>
        <p className="mb-6 py-4">
          Are you sure you want to delete <strong>{animalName}</strong>? This action cannot be undone.
        </p>

        {mutation.isError && (
          <p className="text-red-600 mb-4">Failed to delete animal</p>
        )}

        <div className="flex space-x-4 py-4">
          <button
            onClick={() => mutation.mutate()}
            disabled={mutation.isPending}
            className="font-bold bg-red-600 px-4 py-2 rounded hover:bg-red-700 disabled:bg-gray-400 cursor-pointer"
          >
            {mutation.isPending ? 'Deleting...' : 'Delete'}
          </button>
          <button
            onClick={onClose}
            disabled={mutation.isPending}
            className="px-4 py-2 rounded hover:underline cursor-pointer"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
    </>
  )
}