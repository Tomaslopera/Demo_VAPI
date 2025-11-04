import { useState } from "react";
import { VapiWidget } from "@vapi-ai/client-sdk-react";
import "./App.css";
import siste1 from "./assets/siste1.png";

export default function App() {
  const [mode, setMode] = useState("chat");
  const publicKey = import.meta.env.VITE_VAPI_PUBLIC_KEY;
  const assistantId = import.meta.env.VITE_VAPI_ASSISTANT_ID;

  return (
    <div className="page">
      <section className="hero-sistecredito">
        <div className="hero-content">
          <div className="hero-text">
            <h1>Solicita tu crédito</h1>
            <p>
              Dile sí a todo lo que quieras comprar. En menos de 5 minutos
              puedes solicitar y activar tu crédito.
            </p>
          </div>
          <div className="hero-image">
            <img
              src={siste1}
              alt="Persona usando celular"
              className="hero-persona"
            />
          </div>
        </div>
      </section>

      <section className="como-solicitar">
        <h2>
          ¿Cómo solicitar <span>tu crédito?</span>
        </h2>
        <p>Elige el canal que prefieras para hacer la solicitud.</p>

        <div className="cards-container">
          <div className="info-card">
            <img src="https://cdn-icons-png.flaticon.com/512/84/84401.png" alt="Web" />
            <h3>Web</h3>
            <p>Consíguelo fácil y rápido diligenciando el formulario.</p>
          </div>

          <div className="info-card">
            <img src="https://cdn-icons-png.flaticon.com/512/15/15874.png" alt="App" />
            <h3>App</h3>
            <p>Descárgala y encuentra todo en un solo lugar.</p>
          </div>

          <div className="info-card">
            <img src="https://cdn-icons-png.flaticon.com/512/3721/3721978.png" alt="Punto de venta" />
            <h3>Punto de venta</h3>
            <p>Acércate a nuestros almacenes aliados y solicítalo.</p>
          </div>
        </div>
      </section>

      <VapiWidget
        publicKey={publicKey}
        assistantId={assistantId}
        mode="voice"
        theme="light"
        size="compact"
        position="bottom-right"
        openByDefault={true}
        voiceShowTranscript={true}
        title="Agente de Renegociación"
        chatPlaceholder=""
        onMessage={(msg) => console.log("MSG:", msg)}
        onVoiceEnd={(meta) => console.log("Voice end:", meta)}
        onError={(e) => console.error(e)}
      />
    </div>
  );
}