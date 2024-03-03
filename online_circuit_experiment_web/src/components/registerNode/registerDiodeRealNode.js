import ImageNode from "@/components/Node/ImageNode";
export default function registerDiodeRealNode(lf) {
    lf.register('diode_real', () => {

        class Node extends ImageNode.view {
            getImageHref () {
                return require('../circuit_component_images/diode_real.png');
            }
        }
        class Model extends ImageNode.model {
            initNodeData(data) {
                super.initNodeData(data)
                var wid_div_height = 1.0424710424710424
                this.height=100
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
                        x: x-0.404*width,
                        y: y-0.078*height,
                        type: 'P',
                        edgeAddable: true, // 控制锚点是否可以从此锚点手动创建连线。默认为true。
                        id: `${id}_P`
                    },
                    {
                        x: x+0.450*width,
                        y: y+0.431*height,
                        type: 'N',
                        edgeAddable: true, // 控制锚点是否可以从此锚点手动创建连线。默认为true。
                        id: `${id}_N`
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
