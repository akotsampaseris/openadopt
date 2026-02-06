import { useQuery } from "@tanstack/react-query";
import { useState } from "react";
import { useAuth } from "../../context/AuthContext";
import { getAnimals } from "../../api/animals";
import { Link } from "react-router-dom";

export default function AnimalsPage() {
    const { accessToken } = useAuth();
    const [skip, setSkip] = useState(0);
    const [limit, setLimit] = useState(8);

    const { data, isLoading, error } = useQuery({
        queryKey: ["animals", skip, limit],
        queryFn: () => getAnimals(accessToken!, skip, limit),
        enabled: !!accessToken,
    });

    const total: number = data?.total ? data.total : 0;

    if (isLoading) return <div className="p-8">Loading...</div>;
    if (error)
        return <div className="p-8 text-red-600">Error loading animals</div>;

    return (
        <div className="p-8">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold">Animals</h1>
                <Link
                    to="/admin/animals/new"
                    className="bg-blue-800 px-4 py-2 rounded hover:bg-blue-700"
                >
                    Add Animal
                </Link>
            </div>

            <div className="py-8 grid lg:grid-cols-4 grid-cols-1">
                {total == 0 ? (
                    <div className="px-4 py-4">
                        <p>There are no animals yet. Create one.</p>
                    </div>
                ) : (
                    ""
                )}
                {data?.items.map((animal) => (
                    <div key={animal.id} className="flex-wrap py-8 mx-auto">
                        <Link to={`/admin/animals/${animal.id}`}>
                            {animal.primary_photo_url ? (
                                <img
                                    src={animal.primary_photo_url}
                                    alt={animal.name}
                                    className="w-64 h-64 object-cover rounded-xl"
                                />
                            ) : (
                                <div className="w-64 h-64 bg-gray-300 rounded-xl mb-2 flex items-center justify-center">
                                    <p className="text-gray-800">
                                        No primary photo
                                    </p>
                                </div>
                            )}
                        </Link>
                        <h2 className="px-6 py-2 text-2xl text-center">
                            {animal.name}
                        </h2>
                        <div className="flex gap-4 justify-center">
                            <p className="">{animal.species}</p>
                            <p className="">{animal.gender}</p>
                            <p className="">
                                {animal.age} {animal.age_unit}
                            </p>
                        </div>
                    </div>
                ))}
            </div>

            {/* Pagination */}
            <div className="mt-4 flex justify-between items-center">
                <div>
                    Showing {total > 0 ? skip + 1 : 0} -{" "}
                    {skip + limit < total ? skip + limit : total} of {total}
                </div>
                <div className="space-x-4">
                    <button
                        onClick={() => setSkip((skip) => skip - limit)}
                        disabled={skip === 0}
                        className="py-2 rounded hover:underline disabled:opacity-50 cursor-pointer"
                    >
                        Previous
                    </button>
                    <button
                        onClick={() => setSkip((skip) => skip + limit)}
                        disabled={!data || skip + limit >= data.total}
                        className="py-2 rounded hover:underline disabled:opacity-50 cursor-pointer"
                    >
                        Next
                    </button>
                </div>
            </div>
        </div>
    );
}
