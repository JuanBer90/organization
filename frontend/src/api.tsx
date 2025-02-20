import {Manager} from "./hooks/useEmployees";
import axios from "axios";
const API_BASE_URL = "http://localhost:8000/api";

console.log(API_BASE_URL)
export const fetchEmployees = async (): Promise<Manager[]> => {
    const { data } = await axios.get<Manager[]>(`${API_BASE_URL}/employees`);
    return data;
};

export const updateManager = async (employeeId:number, managerId: number | null ): Promise<boolean> => {
    try {
        await axios.put(`${API_BASE_URL}/employees/${employeeId}/manager/`, {
            manager_id: managerId
        });
        console.log(`unAssign employee ${employeeId}}`);
        return true;
    } catch (error) {
        console.error("Error updating manager:", error);
        return false;
    }
}

export const deleteEmployee = async (employeeId:number ): Promise<boolean> => {
    try {
        await axios.delete(`${API_BASE_URL}/employees/${employeeId}`);
        console.log(`deleted employee ${employeeId}}`);
        return true;
    } catch (error) {
        console.error(`Error deleting employee ${employeeId}:`, error);
        return false;
    }
}



