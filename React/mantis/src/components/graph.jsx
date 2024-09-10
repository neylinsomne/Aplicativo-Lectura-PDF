import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884d8'];

const GraphComponent = () => {
  const [data, setData] = useState([]);
  const [graphType, setGraphType] = useState('');

  const fetchData = async (endpoint) => {
    try {
      const response = await axios.get(`http://localhost:8000/api/${endpoint}`);
      setData(response.data);
      setGraphType(endpoint);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const renderGraph = () => {
    switch (graphType) {
      case 'aerolineas-pasajeros':
      case 'destinos-populares':
        return (
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey={graphType === 'aerolineas-pasajeros' ? 'nombre_aerolinea' : 'destino'} />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey={graphType === 'aerolineas-pasajeros' ? 'total_pasajeros' : 'total_vuelos'} fill="#8884d8" />
            </BarChart>
          </ResponsiveContainer>
        );
      case 'vuelos-por-mes':
        return (
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={data}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="mes" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="total_vuelos" fill="#82ca9d" />
            </BarChart>
          </ResponsiveContainer>
        );
      case 'ocupacion-vuelos':
        return (
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={data}
                cx="50%"
                cy="50%"
                labelLine={false}
                outerRadius={80}
                fill="#8884d8"
                dataKey="pasajeros"
                nameKey="id"
                label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
              >
                {data.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        );
      default:
        return <p>Select a graph type</p>;
    }
  };

  return (
    <div>
      <div>
        <button onClick={() => fetchData('aerolineas-pasajeros')}>Aerolíneas y Pasajeros</button>
        <button onClick={() => fetchData('vuelos-por-mes')}>Vuelos por Mes</button>
        <button onClick={() => fetchData('destinos-populares')}>Destinos Populares</button>
        <button onClick={() => fetchData('ocupacion-vuelos')}>Ocupación de Vuelos</button>
      </div>
      {renderGraph()}
    </div>
  );
};

export default GraphComponent;