import { Component, type ErrorInfo, type ReactNode } from 'react'

interface ErrorBoundaryProps {
  children: ReactNode
  /** Si se define, se usa en vez de la tarjeta a pantalla completa (para boundaries por panel). */
  titulo?: string
  compacto?: boolean
}

interface ErrorBoundaryState {
  error: Error | null
  componentStack: string | null
}

/**
 * Atrapa excepciones de render, ciclo de vida y constructores de su subárbol.
 *
 * NO atrapa: manejadores de eventos, setTimeout/async, ni el onmessage del WebSocket
 * (esos se manejan con try/catch en useEvolutionSocket y con los listeners globales
 * de main.tsx). Nunca renderiza null: una pantalla en blanco es indiagnosticable.
 */
export class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  state: ErrorBoundaryState = { error: null, componentStack: null }

  static getDerivedStateFromError(error: Error): Partial<ErrorBoundaryState> {
    return { error }
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error('[ErrorBoundary]', error, info.componentStack)
    this.setState({ componentStack: info.componentStack ?? null })
  }

  private reiniciar = () => {
    this.setState({ error: null, componentStack: null })
  }

  render() {
    const { error, componentStack } = this.state
    if (!error) return this.props.children

    const mensaje = error.message || String(error)

    if (this.props.compacto) {
      return (
        <div className="error-card error-card-compacto">
          <p className="error-card-titulo">{this.props.titulo ?? 'No se pudo mostrar este panel'}</p>
          <pre className="error-card-mensaje">{mensaje}</pre>
          <button type="button" className="boton boton-tinted" onClick={this.reiniciar}>
            Reintentar
          </button>
        </div>
      )
    }

    return (
      <div className="error-pantalla">
        <div className="error-card">
          <div className="error-card-icono" aria-hidden="true">
            !
          </div>
          <h1 className="error-card-titulo">{this.props.titulo ?? 'Algo salió mal'}</h1>
          <p className="error-card-descripcion">
            La aplicación encontró un error y no pudo continuar. El detalle exacto está abajo.
          </p>
          <pre className="error-card-mensaje">{mensaje}</pre>
          {componentStack && (
            <details className="error-card-detalles">
              <summary>Traza de componentes</summary>
              <pre className="error-card-mensaje">{componentStack}</pre>
            </details>
          )}
          <div className="error-card-acciones">
            <button type="button" className="boton boton-filled" onClick={this.reiniciar}>
              Reintentar
            </button>
            <button type="button" className="boton boton-plain" onClick={() => window.location.reload()}>
              Recargar página
            </button>
          </div>
        </div>
      </div>
    )
  }
}
