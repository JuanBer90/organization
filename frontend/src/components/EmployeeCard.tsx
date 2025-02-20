import { Box, Typography, IconButton } from "@mui/material";
// @ts-ignore
const EmployeeCard = ({ employee, onDelete }) => {
    return (
        <Box
            sx={{
                margin: 1,
                textAlign: "center",
                position: "relative", // Necesario para posicionar el ícono
                padding: 2,
                border: "1px solid #ddd",
                borderRadius: 2,
                boxShadow: 2,
                backgroundColor: "white",
            }}
        >
            {/* Botón de eliminar en la esquina superior derecha */}
            <IconButton
                size="small"
                onClick={() => onDelete(employee.id)}
                sx={{
                    position: "absolute",
                    top: 4,
                    right: 4,
                }}
            >
                x
                {/*<DeleteIcon fontSize="small" />*/}
            </IconButton>

            {/* Contenido */}
            <Typography variant="h6">#{employee.id} - {employee.name}</Typography>
            <Typography variant="body2" color="textSecondary">
                {employee.title}
            </Typography>
        </Box>
    );
};

export default EmployeeCard;
