export default function registerPolyline (lf) {
  lf.register('polyline', ({ PolylineEdge, PolylineEdgeModel}) => {
    class ConnectionLineModel extends PolylineEdgeModel {
      constructor (data, graphModel) {
        super(data, graphModel)
      }
    }
    class ConnectionLineView extends PolylineEdge {
      getArrow () {
        //const { stroke } = model.getEdgeStyle()
        return null
      }
    }
    return {
      view: ConnectionLineView,
      model: ConnectionLineModel
    }
  })
}
