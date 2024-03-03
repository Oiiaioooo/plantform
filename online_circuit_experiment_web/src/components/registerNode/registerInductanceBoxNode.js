import ImageNode from "@/components/Node/ImageNode";
export default function registerInductanceBoxNode(lf) {
    lf.register('inductance_box', () => {

        class Node extends ImageNode.view {
            getImageHref () {
                return require('../circuit_component_images/inductance_box_real.png');
            }
        }
        class Model extends ImageNode.model {
            initNodeData(data) {
                super.initNodeData(data)
                var wid_div_height =  1.01
                this.height=250
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
                        x:  x-0.172*width   ,
                        y: y-0.377*height,
                        type: 'P',
                        edgeAddable: true, // 控制锚点是否可以从此锚点手动创建连线。默认为true。
                        id: `${id}_P`
                    },
                    {
                        x:  x+0.160*width,
                        y:y-0.377*height,
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
