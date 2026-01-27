import { apiClient } from './client'

export interface Animal {
  id: number
  created_by_id: number
  name: string
  species: string
  breed?: string
  age: number
  age_unit: string
  gender: string
  size?: string
  description?: string
  primary_photo_url?: string
  extra_photos_url?: string
  medical_notes?: string
  behavioral_notes?: string
  adoption_status: string
  current_location?: string
  created_at: string
  updated_at: string
}

export interface CreateAnimalData {
  name: string
  species: string
  breed?: string
  age: number
  age_unit: string
  gender: string
  size?: string
  description?: string
  primary_photo_url?: string
  extra_photos_url?: string
  medical_notes?: string
  behavioral_notes?: string
  adoption_status?: string
  current_location: string | null
}

export interface PaginatedAnimalsResponse {
  total: number
  skip: number
  limit: number
  items: Animal[]
}

export async function getAnimals(
  accessToken: string,
  skip: number = 0,
  limit: number = 50
): Promise<PaginatedAnimalsResponse> {
  const { data } = await apiClient.get('/admin/animals', {
    headers: { Authorization: `Bearer ${accessToken}` },
    params: { skip, limit }
  })
  return data
}

export async function getAnimal(accessToken: string, id: number): Promise<Animal> {
  const { data } = await apiClient.get(`/admin/animals/${id}`, {
    headers: { Authorization: `Bearer ${accessToken}` }
  })
  return data
}

export async function createAnimal(
  accessToken: string,
  animalData: CreateAnimalData
): Promise<Animal> {
  const { data } = await apiClient.post('/admin/animals', animalData, {
    headers: { Authorization: `Bearer ${accessToken}` }
  })
  return data
}

export async function updateAnimal(
  accessToken: string,
  id: number,
  animalData: Partial<CreateAnimalData>
): Promise<Animal> {
  const { data } = await apiClient.patch(`/admin/animals/${id}`, animalData, {
    headers: { Authorization: `Bearer ${accessToken}` }
  })
  return data
}

export async function deleteAnimal(accessToken: string, id: number): Promise<void> {
  await apiClient.delete(`/admin/animals/${id}`, {
    headers: { Authorization: `Bearer ${accessToken}` }
  })
}