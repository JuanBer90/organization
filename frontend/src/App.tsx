import React from "react";
import {AppBar, Toolbar, Typography, Container, Grid, Paper, Box} from "@mui/material";
import CreateEmployeeForm from "./components/CreateEmployeeForm";
import OrgChart from "./components/OrgChart";

const App = () => {
    return (
        <>
            {/* Navbar */}
            <AppBar position="static">
                <Toolbar>
                    <Typography variant="h6" sx={{ flexGrow: 1, textAlign: "center" }}>
                        Organization Chart
                    </Typography>
                </Toolbar>
            </AppBar>

            {/* Contenido */}
            <Box
                sx={{
                    display: "flex",
                    justifyContent: "center",
                    alignItems: "center",
                    minHeight: "90vh", // Ajusta la altura para que se vea bien
                }}
            >
                <Grid
                    container
                    spacing={2}
                    justifyContent="center"
                    alignItems="center"
                    style={{ minHeight: "100vh" }} // Centrado vertical
                >
                    <Grid item xs={12} md={4}>
                        <Paper elevation={3} style={{ padding: 20, textAlign: "center" }}>
                            <CreateEmployeeForm />
                        </Paper>
                    </Grid>

                    <Grid item xs={12} md={8}>
                            <OrgChart />
                    </Grid>
                </Grid>
            </Box>
        </>
    );
};

export default App;
