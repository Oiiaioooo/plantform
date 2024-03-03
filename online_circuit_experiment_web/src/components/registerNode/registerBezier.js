export default function registerBezier (lf) {
    lf.register('bezier', ({ BezierEdge, BezierEdgeModel }) => {
        class ConnectionLineModel extends BezierEdgeModel {
            constructor (data, graphModel) {
                super(data, graphModel)
                this.zIndex = 1
            }
            getData() {
                const data = super.getData();
                data.sourceAnchorId = this.sourceAnchorId;
                data.targetAnchorId = this.targetAnchorId;
                return data;
            }
        }
        class ConnectionLineView extends BezierEdge {

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
