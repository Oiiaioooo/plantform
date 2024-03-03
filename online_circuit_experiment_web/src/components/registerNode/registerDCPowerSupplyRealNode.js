import ImageNode from "@/components/Node/ImageNode";
export default function registerDCPowerSupplyRealNode(lf) {
    lf.register('dc_power_supply_real', () => {

        class Node extends ImageNode.view {
            getImageHref () {
                return require('../circuit_component_images/DC_Power_Supply_real.png');
            }
        }
        class Model extends ImageNode.model {
            initNodeData(data) {
                super.initNodeData(data)
                var wid_div_height = 1.48
                this.height=180
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
                        x: x-0.183*width ,
                        y: y+0.310*height,
                        type: 'HI1',
                        edgeAddable: true, // 控制锚点是否可以从此锚点手动创建连线。默认为true。
                        id: `${id}_HI1`
                    },
                    {
                        x:x-0.106*width,
                        y: y+0.310*height,
                        type: 'LO1',
                        id: `${id}_LO1`
                    },
                    {
                        x: x+0.040*width,
                        y: y+0.310*height,
                        type: 'HI2',
                        edgeAddable: true, // 控制锚点是否可以从此锚点手动创建连线。默认为true。
                        id: `${id}_HI2`
                    },
                    {
                        x: x+0.115*width ,
                        y: y+0.310*height,
                        type: 'LO2',
                        id: `${id}_LO2`
                    },
                    {
                        x:  x+0.195*width,
                        y:y+0.310*height,
                        type: 'HI3',
                        edgeAddable: true, // 控制锚点是否可以从此锚点手动创建连线。默认为true。
                        id: `${id}_HI3`
                    },
                    {
                        x:x+0.269*width,
                        y: y+0.310*height,
                        type: 'LO3',
                        id: `${id}_LO3`
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
