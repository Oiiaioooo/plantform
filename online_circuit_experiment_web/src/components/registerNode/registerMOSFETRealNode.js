import ImageNode from "@/components/Node/ImageNode";
export default function registerMOSFETRealNode(lf) {
    lf.register('MOSFET_real', () => {

        class Node extends ImageNode.view {
            getImageHref () {
                return require('../circuit_component_images/MOSFET.png');
            }
        }
        class Model extends ImageNode.model {
            initNodeData(data) {
                super.initNodeData(data)
                var wid_div_height = 0.7171916010498688
                this.height=160
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
                        x: x-0.410*width  ,
                        y: y+0.419*height,
                        type: 'G',
                        edgeAddable: true, // 控制锚点是否可以从此锚点手动创建连线。默认为true。
                        id: `${id}_G`
                    },
                    {
                        x: x-0.312*width,
                        y: y+0.441*height,
                        type: 'D',
                        edgeAddable: true, // 控制锚点是否可以从此锚点手动创建连线。默认为true。
                        id: `${id}_D`
                    },
                    {
                        x: x-0.221*width,
                        y: y+0.466*height,
                        type: 'S',
                        edgeAddable: true, // 控制锚点是否可以从此锚点手动创建连线。默认为true。
                        id: `${id}_S`
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
