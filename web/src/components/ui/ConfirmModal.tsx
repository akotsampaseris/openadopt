interface ConfirmModalProps {
  isOpen: boolean
  title: string
  message: string
  confirmText?: string
  cancelText?: string
  onConfirm: () => void
  onCancel: () => void
  isDangerous?: boolean
}

export default function ConfirmModal({
  isOpen,
  title,
  message,
  confirmText = 'Confirm',
  cancelText = 'Cancel',
  onConfirm,
  onCancel,
  isDangerous = false
}: ConfirmModalProps) {
  if (!isOpen) return null

  return (
    <>
    <div className="fixed bg-black opacity-50 inset-0"></div>
    <div className="fixed inset-0 flex items-center justify-center z-50">
      <div className="bg-gray-700 shadow-black shadow-2xl rounded-lg p-6 max-w-2xl w-full mx-4">
        <h2 className="text-xl font-bold mb-4 border-b py-4">{title}</h2>
        <p className="mb-6 py-4">{message}</p>
        <div className="flex space-x-4 py-4">
          <button
            onClick={onConfirm}
            className={`px-4 py-2 rounded font-bold text-white cursor-pointer ${
              isDangerous 
                ? 'bg-red-500 hover:bg-red-600' 
                : 'bg-blue-500 hover:bg-blue-600'
            }`}
          >
            {confirmText}
          </button>
          <button
            onClick={onCancel}
            className="px-4 py-2 rounded hover:underline cursor-pointer"
          >
            {cancelText}
          </button>
        </div>
      </div>
    </div>
    </>
  )
}