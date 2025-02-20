import { useQuery } from "@tanstack/react-query";
import {fetchEmployees} from "../api"



interface BaseEmployee {
    id: number;
    name: string;
    title: string;
    manager_id: number | null;
}

export interface Employee extends BaseEmployee {}

export interface Manager extends BaseEmployee {
    employees: Employee[];
}


export const useEmployees = () => {
    return useQuery({ queryKey: ["employees"], queryFn: fetchEmployees });
};
