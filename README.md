# Agente de Renegociaciones Sistecrédito VAPI

**Integración del widget de `@vapi‑ai/client‑sdk‑react` (VAPI) para renegociación de créditos**

[Public Link](https://sistecreditorenegociacion.netlify.app/)

[![Netlify Status](https://api.netlify.com/api/v1/badges/625a23ce-4f4d-4aeb-ab20-a6a9c1b334ef/deploy-status)](https://app.netlify.com/projects/sistecreditorenegociacion/deploys)

## Integración Widget

> Instalación dependencias
```bash
npm install @vapi-ai/client-sdk-react @vapi-ai/web
```

> Implementación React
```bash
import { useState } from "react";
import { VapiWidget } from "@vapi-ai/client-sdk-react";
import "./App.css";

export default function App() {
  const [mode, setMode] = useState("chat");
  const publicKey = import.meta.env.VITE_VAPI_PUBLIC_KEY;
  const assistantId = import.meta.env.VITE_VAPI_ASSISTANT_ID;

  return (
    <div className="page">
      {/* … Diseño de landing … */}
      <VapiWidget
        publicKey={publicKey}
        assistantId={assistantId}
        mode={mode}
        theme="dark"
        size="compact"
        position="bottom-right"
        openByDefault={true}
        voiceShowTranscript={true}
        title="Agente de Renegociación"
        chatPlaceholder="Cuéntame cómo quieres ponerte al día…"
        onMessage={(m) => console.log("Mensaje del usuario:", m)}
        onError={(e) => console.error("Error del widget:", e)}
      />
    </div>
  );
}
```


## DummyClient API

API simple en FastAPI para consultar clientes en mora desde un CSV.  
Diseñada para integrarse con un agente en Vapi a través de HTTP Tool.

### Endpoints

- **GET /** → prueba de estado
- **GET /buscar_cliente?nombre=<nombre>&identificacion=<id>**
  - Busca un cliente por nombre e identificación.
  - Respuesta:
    ```json
    {
      "found": true,
      "cliente": {
        "nombre": "Pedro Sierra",
        "id": "87654321",
        "credit_amount": 2500.0,
        "credit_date": "2025-08-30",
        "credit_interest": 3.0
      }
    }
    ```

### Despliegue en Railway

1. Subir repo a GitHub.
2. En Railway → **New Project** → **Deploy from GitHub Repo**.
3. Railway detectará `Procfile` y levantará el servicio automáticamente.
4. Obtendrás un dominio público tipo `https://dummyclient.up.railway.app`.
