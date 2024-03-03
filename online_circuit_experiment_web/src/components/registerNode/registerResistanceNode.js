export default function registerResistanceNode (lf) {
    lf.register('resistance', ({ PolygonNode, PolygonNodeModel, h }) => {
        class Node extends PolygonNode {

            getShape () {
                const {model} = this.props
                const { x, y, width, height } = model;
                const {stroke} = model.getNodeStyle()
                return h(
                    'svg',
                    {
                        x:x - width / 2,
                        y: y - height / 2,
                        width: 100,
                        height: 100,
                        viewBox: '0 0 100 100'
                    },
                    h(
                        'path',
                        {
                            fill:stroke,
                            stroke:"black",
                            strokeWidth:'5',
                            d: "M0 50 L30 50 L30 40 L70 40 L70 50L100 50 M30 50 L30 60 L70 60 L70 50"
                        }
                    )
                )
            }
        }
        class Model extends PolygonNodeModel {
            constructor (data, graphModel) {
                data.text = {
                    value: (data.text && data.text.value) || '',
                    x: data.x,
                    y: data.y + 50
                }
                super(data, graphModel)
                // 右键菜单自由配置，也可以通过边的properties或者其他属性条件更换不同菜单
                this.menu = [
                    {
                        className: 'lf-menu-delete',
                        text: 'delete',
                        callback (node) {
                            // const comfirm = window.confirm('你确定要删除吗？')
                            lf.deleteNode(node.id)
                        }
                    },
                    {
                        text: 'edit',
                        className: 'lf-menu-item',
                        callback (node) {
                            lf.editText(node.id)
                        }
                    },
                    {
                        text: 'copy',
                        className: 'lf-menu-item',
                        callback (node) {
                            lf.cloneNode(node.id)
                        }
                    }
                ]
            }
            initNodeData(data) {
                super.initNodeData(data)
            }
            // 自定义锚点样式
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

                } = this;
                return [
                    {
                        x: x-width/2,
                        y: y,
                        type: 'P',
                        edgeAddable: true, // 控制锚点是否可以从此锚点手动创建连线。默认为true。
                        id: `${id}_P`
                    },
                    {
                        x: x+width/2,
                        y: y,
                        type: 'N',
                        id: `${id}_N`
                    },
                ]
            }
        }
        return {
            view: Node,
            model: Model
        }
    })
}
