import { useQuery } from "@tanstack/react-query";
import axios from "axios";

export interface Employee {
    id: number;
    name: string;
    title: string;
    manager_id: number | null;
}

const fetchEmployees = async (): Promise<Employee[]> => {
    const { data } = await axios.get<Employee[]>("http://127.0.0.1:8000/api/employees");
    return data;
};

export const useEmployees = () => {
    return useQuery({ queryKey: ["employees"], queryFn: fetchEmployees });
};
