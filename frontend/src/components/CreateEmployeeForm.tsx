import React, { useState } from "react";
import { useMutation, useQueryClient } from "@tanstack/react-query";
import axios from "axios";
import { TextField, Button, Box, Typography, CircularProgress, Alert } from "@mui/material";

interface Employee {
    id: number;
    name: string;
    title: string;
    manager_id: number | null;
}

const API_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";

const createEmployee = async (employee: Omit<Employee, "id">) => {
    const { data } = await axios.post<Employee>(`${API_URL}/api/employees`, employee);
    return data;
};

const CreateEmployeeForm: React.FC = () => {
    const queryClient = useQueryClient();
    const [name, setName] = useState("");
    const [title, setTitle] = useState("");
    const [managerId, setManagerId] = useState<number | null>(null);
    const [errorMessage, setErrorMessage] = useState("");

    const mutation = useMutation({
        mutationFn: createEmployee,
        onSuccess: () => {
            // @ts-ignore
            queryClient.invalidateQueries(["employees"]); // Actualiza la lista de empleados
            setName("");
            setTitle("");
            setManagerId(null);
            setErrorMessage("");
        },
        onError: (error: any) => {
            setErrorMessage(error.response?.data?.detail || "Error creating employee");
        }
    });

    const handleSubmit = (event: React.FormEvent) => {
        event.preventDefault();
        mutation.mutate({ name, title, manager_id: managerId });
    };

    return (
        <Box sx={{ maxWidth: 400, margin: "auto", padding: 2 }}>
            <Typography variant="h4" sx={{ flexGrow: 1, textAlign: "center" }}>
                Create New Employee
            </Typography>

            {errorMessage && <Alert severity="error">{errorMessage}</Alert>}

            <form onSubmit={handleSubmit}>
                <TextField
                    label="Name"
                    fullWidth
                    required
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                    sx={{ marginBottom: 2 }}
                />
                <TextField
                    label="Title"
                    fullWidth
                    required
                    value={title}
                    onChange={(e) => setTitle(e.target.value)}
                    sx={{ marginBottom: 2 }}
                />
                <Button type="submit" variant="contained" fullWidth >
                   "Create Employee"
                </Button>
            </form>
        </Box>
    );
};

export default CreateEmployeeForm;
