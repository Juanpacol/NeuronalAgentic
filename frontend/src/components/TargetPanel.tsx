/** Imagen objetivo, en una caja del mismo tamaño/aspect-ratio (16:9) que GenomeCanvas, para comparación visual. */
export function TargetPanel() {
  return (
    <div className="canvas-box">
      <img src="/target.jpg" alt="Imagen objetivo" className="target-image" />
    </div>
  )
}
