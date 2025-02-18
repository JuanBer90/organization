import React from "react";
import { Container } from "@mui/material";
import CreateEmployeeForm from "./components/CreateEmployeeForm";
import OrgChart from "./components/OrgChart";

const App: React.FC = () => {
    return (
        <Container
            sx={{
                display: 'flex',
                justifyContent: 'center',  // Centra horizontalmente
                alignItems: 'center',      // Centra verticalmente
                height: '100vh',            // Ocupa toda la altura de la ventana
            }}>

            <CreateEmployeeForm />

            <OrgChart />
        </Container>
    );
};

export default App;
