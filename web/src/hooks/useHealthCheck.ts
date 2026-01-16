import { useQuery } from '@tanstack/react-query';
import { apiClient } from '../api/client';


interface HealthResponse {
    status: string
}

export function useHealthCheck() {
    return useQuery<HealthResponse>({
        queryKey: ['health'],
        queryFn: async () => {
            const { data } = await apiClient.get('/health');
            return data;

        },
        refetchInterval: 30000,
        retry: 3,
    })
}