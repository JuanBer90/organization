import React, { useState, useEffect } from "react";
import { DragDropContext, Droppable, Draggable, DropResult } from "@hello-pangea/dnd";
import { Box, Typography, Paper, Grid } from "@mui/material";
import EmployeeCard from "./EmployeeCard";
import { useEmployees, Manager, Employee } from "../hooks/useEmployees";
import {deleteEmployee, updateManager} from "../api";
import { useQueryClient } from "@tanstack/react-query";

const OrgChart: React.FC = () => {
    const [groups, setGroups] = useState<Manager[]>([]);
    const [independentItems, setIndependentItems] = useState<Employee[]>([]);
    const queryClient = useQueryClient();

    const { data: items = [], isLoading, refetch } = useEmployees();


    useEffect(() => {
        const grouped: Manager[] = [];
        const independent: Employee[] = [];

        items.forEach(item => {
            if (item.employees.length > 0) {
                grouped.push(item);
            } else {
                independent.push(item);
            }
        });

        setGroups(grouped);
        setIndependentItems(independent);
    }, [items]);

    const unAssign = async (employeeId: number) => {
        const success = await updateManager(employeeId, null);
        if (success){
            await refetch();
        }

    }

    const removeEmployee = async (employeeId: number) => {
        const success = await deleteEmployee(employeeId);
        if (success){
            await refetch();
        }

    }



    const updateManagers = async ( sourceId: number, managerId: number | null )=>{

        const success = await updateManager(sourceId, managerId);
        console.log("updated", success)
        if (success){
            queryClient.invalidateQueries(["managers", sourceId]); // Force refetch

        }

    }


    const handleDragEnd = async (result: DropResult) =>  {
        const { source, destination } = result;
        if (!destination || source.droppableId === destination.droppableId) return;


        let movedItem: Employee | undefined;
        let newIndependentItems = [...independentItems];
        let newGroups = [...groups];

        if (source.droppableId === "items") {
            const itemIndex = newIndependentItems.findIndex(item => item.id === parseInt(result.draggableId));
            if (itemIndex !== -1) {
                movedItem = newIndependentItems[itemIndex];
                newIndependentItems.splice(itemIndex, 1);
            }
        } else {
            const sourceGroupIndex = newGroups.findIndex(group => group.id === parseInt(source.droppableId));
            if (sourceGroupIndex !== -1) {
                const sourceGroup = newGroups[sourceGroupIndex];
                const itemIndex = sourceGroup.employees.findIndex(item => item.id === parseInt(result.draggableId));
                if (itemIndex !== -1) {
                    movedItem = sourceGroup.employees[itemIndex];
                    newGroups[sourceGroupIndex] = {
                        ...sourceGroup,
                        employees: sourceGroup.employees.filter((_, i) => i !== itemIndex),
                    };
                }
            }
        }

        if (!movedItem) return;

        if (destination.droppableId === "new-group-zone") {
            newGroups.push({
                id: movedItem.id,
                name: movedItem.name,
                manager_id: movedItem.manager_id,
                title: movedItem.title,
                employees: [],
            });
        } else {
            const destinationGroupIndex = newGroups.findIndex(group => group.id === parseInt(destination.droppableId));
            if (destinationGroupIndex !== -1) {
                newGroups[destinationGroupIndex] = {
                    ...newGroups[destinationGroupIndex],
                    employees: [...newGroups[destinationGroupIndex].employees, movedItem],
                };
                await updateManagers(movedItem.id, newGroups[destinationGroupIndex].id)
                newIndependentItems.push(movedItem);
            } else {
                await updateManagers(movedItem.id, null)
                newIndependentItems.push(movedItem);
            }
            await refetch();
        }

        setIndependentItems(newIndependentItems);
        setGroups(newGroups);
    };

    return (
        <DragDropContext onDragEnd={handleDragEnd}>
            <Grid container spacing={2}>

                <Grid item xs={6}>
                    <Droppable droppableId="items" type="item">
                        {(provided) => (
                            <Paper elevation={3} style={{ padding: 20, textAlign: "center" }}>
                                <Typography variant="h5">Unassigned Employees</Typography>

                                <Box ref={provided.innerRef} {...provided.droppableProps} sx={{ marginTop: 2, padding: 2 }}>
                                    <Grid container spacing={2}>

                                        {independentItems.map((item, index) => (
                                            <Grid item xs={6}>

                                                <Draggable key={item.id} draggableId={item.id.toString()} index={index}>
                                                    {(provided) => (
                                                        <Box ref={provided.innerRef} {...provided.draggableProps} {...provided.dragHandleProps} >
                                                            <EmployeeCard onDelete={(employeeId: number)=>{removeEmployee(employeeId)}}  key={item.id} employee={item}/>
                                                        </Box>
                                                    )}
                                                </Draggable>
                                            </Grid>

                                        ))}
                                    </Grid>

                                    {provided.placeholder}
                                </Box>
                            </Paper>
                        )}

                    </Droppable>
                </Grid>
                <Grid item xs={6}>
                    <Droppable droppableId="parent" type="group" >
                        {(provided) => (
                            <Paper elevation={3} style={{ padding: 20, textAlign: "center" }}>

                                <Box ref={provided.innerRef} {...provided.droppableProps} sx={{ padding: 2, minHeight: 400, marginBottom: 2 }}>
                                    <Typography variant="h5">Managers</Typography>

                                    <Droppable droppableId="new-group-zone" type="item">
                                        {(provided) => (
                                            <Box ref={provided.innerRef} {...provided.droppableProps} sx={{ padding: 2, border: "2px dashed red", minHeight: 80, margin: 10, backgroundColor: "#f8d7da" }}>
                                                <Typography variant="subtitle1">Drop an employee here to promote him as a manager</Typography>
                                                {provided.placeholder}
                                            </Box>
                                        )}
                                    </Droppable>

                                    {groups.map(group => (
                                        <Droppable key={group.id} droppableId={group.id.toString()} type="item">
                                            {(provided) => (
                                                <Box ref={provided.innerRef} {...provided.droppableProps} sx={{ padding: 2, border: "1px dashed gray",  minHeight: 100, margin: 10 }}>
                                                    <Typography variant="subtitle1">{group.name} - {group.title}</Typography>
                                                    {group.employees.map((child, index) => (
                                                        <Draggable key={child.id} draggableId={child.id.toString()} index={index}>
                                                            {(provided) => (
                                                                <Box ref={provided.innerRef} {...provided.draggableProps} {...provided.dragHandleProps} >
                                                                    <EmployeeCard onDelete={(employeeId: number)=>{unAssign(employeeId)}}  key={child.id} employee={child}/>
                                                                </Box>
                                                            )}
                                                        </Draggable>
                                                    ))}
                                                    {provided.placeholder}
                                                </Box>
                                            )}
                                        </Droppable>
                                    ))}

                                    {provided.placeholder}
                                </Box>
                            </Paper>
                        )}
                    </Droppable>
                </Grid>
            </Grid>

        </DragDropContext>
    );
};

export default OrgChart;
