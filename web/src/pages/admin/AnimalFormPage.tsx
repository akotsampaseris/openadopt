import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { useNavigate, useParams } from "react-router-dom";
import { useState } from "react";

import { useAuth } from "../../context/AuthContext";
import { createAnimal, updateAnimal, getAnimal } from "../../api/animals";
import type { CreateAnimalData } from "../../api/animals";
import AnimalForm from "../../components/animals/AnimalForm";

export default function AnimalFormPage() {
  const { id } = useParams();
  const isEdit = !!id;
  const { accessToken } = useAuth();
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  // Fetch animal if editing
  const { data: animal, isLoading } = useQuery({
    queryKey: ["animal", id],
    queryFn: () => getAnimal(accessToken!, Number(id)),
    enabled: isEdit && !!accessToken,
  });

  const mutation = useMutation({
    mutationFn: (data: CreateAnimalData) =>
      isEdit
        ? updateAnimal(accessToken!, Number(id), data)
        : createAnimal(accessToken!, data),
    onSuccess: (animal) => {
      queryClient.invalidateQueries({ queryKey: ["animals"] });
      queryClient.invalidateQueries({ queryKey: ["animal", id] });
      navigate(`/admin/animals/${animal.id}`);
    },
  });

  if (isEdit && isLoading) {
    return <div className="p-8">Loading...</div>;
  }

  return (
    <>
      <div className="p-8 max-w-2xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold">
            {isEdit ? `Edit ${animal?.name}` : "Add Animal"}
          </h1>
        </div>

        <AnimalForm
          animal={animal}
          onSubmit={(data) => mutation.mutate(data)}
          isSubmitting={mutation.isPending}
          onCancel={() => {
            if (isEdit) {
              navigate(`/admin/animals/${animal?.id}`);
            } else {
              navigate(`/admin/animals`);
            }
          }}
        />

        {mutation.isError && (
          <p className="text-red-600 mt-4">Failed to save animal</p>
        )}
      </div>
    </>
  );
}
