import { useEffect, useState } from 'react';
import axios from 'axios';

function App() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/mio')
      .then((response) => {
        setData(response.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Error al conectar con el backend:", err);
        setError("No se pudo conectar con el backend");
        setLoading(false);
      });
  }, []);

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
      <h1>Conexión React a Backend</h1>
      
      {loading && <p>Cargando datos...</p>}
      
      {error && <p style={{ color: 'red' }}>{error}</p>}
      
      {data && (
        <div style={{ background: '#f0f0f0', padding: '15px', borderRadius: '5px' }}>
          <h3>Respuesta del servidor:</h3>
          <pre>{JSON.stringify(data, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;
