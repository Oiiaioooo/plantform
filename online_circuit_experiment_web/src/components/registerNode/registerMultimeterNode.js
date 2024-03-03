import ImageNode from "@/components/Node/ImageNode";
export default function registerMultimeterNode(lf) {
    lf.register('multimeter', () => {

        class Node extends ImageNode.view {
            getImageHref () {
                return require('../circuit_component_images/multimeter.png');
            }
        }
        class Model extends ImageNode.model {
            initNodeData(data) {
                super.initNodeData(data)
                this.width = 85
                this.height = 100
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
                        x: x-width/3.3,
                        y: y+height/4,
                        type: 'HI1',
                        edgeAddable: true, // 控制锚点是否可以从此锚点手动创建连线。默认为true。
                        id: `${id}_HI1`
                    },
                    {
                        x: x-width/500,
                        y: y+height/4.1,
                        type: 'LO',
                        id: `${id}_LO`
                    },
                    {
                        x: x+width/3.3,
                        y: y+height/4,
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
