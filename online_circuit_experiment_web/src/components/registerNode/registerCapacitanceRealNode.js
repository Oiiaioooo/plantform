import ImageNode from "@/components/Node/ImageNode";
export default function registerCapacitanceRealNode(lf) {
    lf.register('capacitance_real', () => {

        class Node extends ImageNode.view {
            getImageHref () {
                return require('../circuit_component_images/capacitance_real.png');
            }
        }
        class Model extends ImageNode.model {
            initNodeData(data) {
                super.initNodeData(data)
                var wid_div_height = 0.44502617801047123
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
                        x: x-0.122*width  ,
                        y: y+0.349*height,
                        type: 'P',
                        edgeAddable: true, // 控制锚点是否可以从此锚点手动创建连线。默认为true。
                        id: `${id}_P`
                    },
                    {
                        x: x+0.269*width,
                        y: y+0.452*height,
                        type: 'P',
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
