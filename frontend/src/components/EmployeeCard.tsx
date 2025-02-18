import React from "react";
import { Card, CardContent, Typography } from "@mui/material";
import { Employee } from "../hooks/useEmployees";

interface EmployeeCardProps {
    employee: Employee;
}

const defaultEmployee: Employee = {
    id: 0,
    name: "Peter",
    title: "Designer",
    manager_id: null
};


const EmployeeCard: React.FC<{ employee?: Employee }> = ({ employee = defaultEmployee }) => {

    return (
        <Card sx={{ width: 200, margin: 1, textAlign: "center" }}>
            <CardContent>
                <Typography variant="h6">{employee.name}</Typography>
                <Typography variant="body2" color="textSecondary">
                    {employee.title}
                </Typography>
            </CardContent>
        </Card>
    );
};

export default EmployeeCard;
