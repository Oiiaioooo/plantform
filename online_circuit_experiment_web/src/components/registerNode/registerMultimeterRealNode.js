import ImageNode from "@/components/Node/ImageNode";
export default function registerMultimeteRealrNode(lf) {
    lf.register('multimeter_real', () => {

        class Node extends ImageNode.view {
            getImageHref () {
                return require('../circuit_component_images/multimeter_real.png');
            }
        }
        class Model extends ImageNode.model {
            initNodeData(data) {
                super.initNodeData(data)
                var wid_div_height = 2.0158
                this.height=150
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
                        x: x+width/2.11,
                        y: y-height/5.7,
                        type: 'HI1',
                        edgeAddable: true, // 控制锚点是否可以从此锚点手动创建连线。默认为true。
                        id: `${id}_HI1`
                    },
                    {
                        x:x+width/2.11,
                        y: y-height/20,
                        type: 'LO',
                        id: `${id}_LO`
                    },
                    {
                        x: x+width/2.11,
                        y: y+height/12,
                        type: 'HI2',
                        edgeAddable: true, // 控制锚点是否可以从此锚点手动创建连线。默认为true。
                        id: `${id}_HI2`
                    }
                ]
            }
        }
        return {
            'view': Node,
            'model': Model
        }
    })
}
