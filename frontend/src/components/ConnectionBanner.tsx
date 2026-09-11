import type { EstadoConexion } from '../lib/tipos'

interface ConnectionBannerProps {
  status: EstadoConexion
  mensajeError: string | null
  onReintentar: () => void
}

/** Banner contextual según el estado de la conexión WebSocket. */
export function ConnectionBanner({ status, mensajeError, onReintentar }: ConnectionBannerProps) {
  if (status === 'waking') {
    return (
      <div className="connection-banner banner-info">
        <p>Despertando el servidor gratuito de Render, puede tardar hasta 50 segundos…</p>
        <div className="progress-indeterminate">
          <div className="progress-indeterminate-bar" />
        </div>
      </div>
    )
  }

  if (status === 'reconnecting') {
    return (
      <div className="connection-banner banner-warning">
        <p>Reconectando…</p>
      </div>
    )
  }

  if (status === 'error') {
    return (
      <div className="connection-banner banner-error">
        <p>{mensajeError ?? 'Ocurrió un error de conexión.'}</p>
        <button type="button" onClick={onReintentar}>
          Reintentar
        </button>
      </div>
    )
  }

  return null
}
