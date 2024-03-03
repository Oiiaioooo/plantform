import ImageNode from "@/components/Node/ImageNode";
export default function registerGNDNode(lf) {
    lf.register('GND', () => {

        class Node extends ImageNode.view {
            getImageHref () {
                return require('../circuit_component_images/GND.png');
            }
        }
        class Model extends ImageNode.model {
            initNodeData(data) {
                super.initNodeData(data)
                var wid_div_height = 1.1149253731343283
                this.height=70
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
                        x: x-0.241*width  ,
                        y: y-0.413*height,
                        type: 'GND',
                        edgeAddable: true, // 控制锚点是否可以从此锚点手动创建连线。默认为true。
                        id: `${id}_GND`
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
