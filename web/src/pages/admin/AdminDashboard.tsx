import { Link } from 'react-router-dom'


export default function AdminDashboardPage () {
    return (
        <>
            <div className="w-fit mx-auto text-green-400 text-2xl">
                Admin Dashboard
            </div>
            <div className="w-fit mx-auto text-green-400 text-2xl">
                <Link 
                    to="/admin/animals"
                    className="text-blue-500 text-2xl px-4 py-2"
                    >
                    My animals
                    </Link>
            </div>
        </>
    )
}