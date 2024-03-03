import ImageNode from "@/components/Node/ImageNode";
export default function registerCapacitanceBoxNode(lf) {
    lf.register('capacitance_box', () => {

        class Node extends ImageNode.view {
            getImageHref () {
                return require('../circuit_component_images/capacitance_box_real.png');
            }
        }
        class Model extends ImageNode.model {
            initNodeData(data) {
                super.initNodeData(data)
                var wid_div_height =  2.601
                this.height=165
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
                        x:  x+0.456*width  ,
                        y: y-0.028*height,
                        type: 'P',
                        edgeAddable: true, // 控制锚点是否可以从此锚点手动创建连线。默认为true。
                        id: `${id}_P`
                    },
                    {
                        x: x+0.458*width ,
                        y:y+0.280*height,
                        type: 'N',
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
