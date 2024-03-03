import ImageNode from "@/components/Node/ImageNode";
export default function registerSignalGeneratorRealNode(lf) {
    lf.register('signal_generator', () => {

        class Node extends ImageNode.view {
            getImageHref () {
                return require('../circuit_component_images/SignalGenerator_real.png');
            }
        }
        class Model extends ImageNode.model {
            initNodeData(data) {
                super.initNodeData(data)
                var wid_div_height = 1.64
                this.height=170
                this.width = this.height*wid_div_height
            }
            getAnchorStyle() {
                const style = super.getAnchorStyle();
                style.hover.r = 10;
                style.hover.fill = "rgb(24, 125, 255)";
                style.hover.stroke = "rgb(24, 125, 255)";
                return style;
            }
            getDefaultAnchor() {
                const {
                    id,
                    x,
                    y,
                    width,
                    height

                } = this;
                return [
                    {
                        x:x+0.008*width,
                        y:y+0.467*height,
                        type: 'CH1P',
                        edgeAddable: true, // 控制锚点是否可以从此锚点手动创建连线。默认为true。
                        id: `${id}_CH1P`
                    },
                    {
                        x:x+0.088*width,
                        y:y+0.467*height,
                        type: 'CH1N',
                        id: `${id}_CH1N`
                    },
                    {
                        x:x+0.153*width,
                        y:y+0.467*height,
                        type: 'CH2P',
                        id: `${id}_CH2P`
                    },
                    {
                        x:x+0.226*width,
                        y:y+0.467*height,
                        type: 'CH2N',
                        id: `${id}_CH2N`
                    },
                ]
            }
        }
        return {
            'view': Node,
            'model': Model
        }
    })
}
