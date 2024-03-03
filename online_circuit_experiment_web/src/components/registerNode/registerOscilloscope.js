import ImageNode from "@/components/Node/ImageNode";
export default function registerOscilloscopeRealNode(lf) {
    lf.register('oscilloscope_real', () => {

        class Node extends ImageNode.view {
            getImageHref () {
                return require('../circuit_component_images/oscilloscope_real.png');
            }
        }
        class Model extends ImageNode.model {
            initNodeData(data) {
                super.initNodeData(data)
                var wid_div_height = 1.782
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
                        x: x+0.143*width  ,
                        y: y+0.442*height,
                        type: 'CH1',
                        edgeAddable: true, // 控制锚点是否可以从此锚点手动创建连线。默认为true。
                        id: `${id}_CH1`
                    },
                    {
                        x: x+0.232*width,
                        y: y+0.438*height,
                        type: 'CH2',
                        edgeAddable: true, // 控制锚点是否可以从此锚点手动创建连线。默认为true。
                        id: `${id}_CH2`
                    },
                    {
                        x: x+0.351*width,
                        y: y+0.288*height,
                        type: 'GND',
                        edgeAddable: true, // 控制锚点是否可以从此锚点手动创建连线。默认为true。
                        id: `${id}_GND`
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
