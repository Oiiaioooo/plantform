import ImageNode from "@/components/Node/ImageNode";
export default function register8720DMNode(lf) {
    lf.register('DM8720', () => {

        class Node extends ImageNode.view {
            getImageHref () {
                return require('../circuit_component_images/8720DM.png');
            }
        }
        class Model extends ImageNode.model {
            initNodeData(data) {
                super.initNodeData(data)
                var wid_div_height =  1.265
                this.height=230
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
                        x:x-0.434*width,
                        y:y-0.337*height,
                        type: 'I1U1',
                        edgeAddable: true, // 控制锚点是否可以从此锚点手动创建连线。默认为true。
                        id: `${id}_I1U1`
                    },
                    {
                        x:x+0.430*width,
                        y:y-0.334*height,
                        type: 'I2',
                        id: `${id}_I2`
                    },
                    {
                        x:x+0.427*width,
                        y:y-0.234*height,
                        type: 'U2',
                        id: `${id}_U2`
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
