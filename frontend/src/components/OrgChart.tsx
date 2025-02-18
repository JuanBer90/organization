import React, { useState, useEffect } from "react";
import { useEmployees } from "../hooks/useEmployees"; // API hook
import { DragDropContext, Droppable, Draggable, DropResult } from "@hello-pangea/dnd";
import { Box, Typography, Paper } from "@mui/material";
import EmployeeCard from "./EmployeeCard";
import axios from "axios";

const OrgChart: React.FC = () => {
    const { data: initialManagers, isLoading } = useEmployees();
    const [managers, setManagers] = useState(initialManagers || []);

    // Update local state when API data is available
    useEffect(() => {
        if (initialManagers) {
            setManagers(initialManagers);
        }
    }, [initialManagers]);

    // Handle Drag & Drop logic
    const handleDragEnd = async (result: DropResult) => {
        const { source, destination } = result;
        if (!destination) return;

        const sourceManagerId = parseInt(source.droppableId);
        const destManagerId = parseInt(destination.droppableId);
        const employeeIndex = source.index;

        // Find the source and destination managers
        const sourceManager = managers.find((m) => m.id === sourceManagerId);
        const destManager = managers.find((m) => m.id === destManagerId);

        if (!sourceManager || !destManager) return;

        // Remove employee from source
        const movedEmployee = sourceManager.employees.splice(employeeIndex, 1)[0];

        // Add employee to destination
        destManager.employees.splice(destination.index, 0, movedEmployee);

        // Update state
        setManagers([...managers]);

        // Send update to the backend
        try {
            await axios.put(`/api/employees/${movedEmployee.id}/manager/`, {
                manager_id: destManager.id
            });
            console.log(`Updated employee ${movedEmployee.id} to manager ${destManager.id}`);
        } catch (error) {
            console.error("Error updating manager:", error);
        }
    };

    if (isLoading) return <Typography>Loading...</Typography>;

    return (
        <DragDropContext onDragEnd={handleDragEnd}>
            <Box sx={{ display: "flex", gap: 2, flexWrap: "wrap", justifyContent: "center", padding: 2 }}>
                {managers.map((manager) => (
                    <Droppable key={manager.id} droppableId={String(manager.id)}>
                        {(provided) => (
                            <Paper
                                ref={provided.innerRef}
                                {...provided.droppableProps}
                                sx={{ padding: 2, minWidth: 250, maxWidth: 300, backgroundColor: "#f8f8f8" }}
                            >
                                <Typography variant="h6" sx={{ fontWeight: "bold", textAlign: "center" }}>
                                    {manager.name} - {manager.title}
                                </Typography>
                                {manager.employees.map((employee, index) => (
                                    <Draggable key={employee.id} draggableId={String(employee.id)} index={index}>
                                        {(provided) => (
                                            <Paper
                                                ref={provided.innerRef}
                                                {...provided.draggableProps}
                                                {...provided.dragHandleProps}
                                                sx={{
                                                    padding: 1,
                                                    margin: "8px 0",
                                                    backgroundColor: "white",
                                                    boxShadow: 2,
                                                    cursor: "grab",
                                                }}
                                            >
                                                <EmployeeCard employee={employee} />
                                            </Paper>
                                        )}
                                    </Draggable>
                                ))}
                                {provided.placeholder}
                            </Paper>
                        )}
                    </Droppable>
                ))}
            </Box>
        </DragDropContext>
    );
};

export default OrgChart;
