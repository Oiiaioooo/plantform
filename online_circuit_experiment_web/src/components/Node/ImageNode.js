import {h} from '@logicflow/core'
import RectNode from "@/components/Node/RectNode";
import {circuitRules} from "@/components/NodeRules/noderules";

// 图片-基础节点
class ImageModel extends RectNode.model {
    initNodeData(data) {
        super.initNodeData(data)
        this.width = 80
        this.height = 60
        this.zIndex = 0

    }

    //    在此处增加规则，因为后面所有的节点继承了这一个节点且，全部使用了super.iniNodeData()因此不会将规则覆盖
    getConnectedSourceRules() {
        const rules = super.getConnectedSourceRules()
        const circuitRulesList = circuitRules()
        for (const i in circuitRulesList) {
            rules.push(circuitRulesList[i])
        }
        return rules
    }
    // getConnectedTargetRules() {
    //     const rules = super.getConnectedTargetRules()
    //     rules.push(circuitRules)
    //     return rules
    // }

    getDefaultAnchor() {
        return []
    }

    getData() {
        const data = super.getData();
        data.Anchors = this.getDefaultAnchor();
        return data;
    }

}


class ImageNode extends RectNode.view {
    getImageHref() {
        return;
    }

    toFront() {
    }

    getResizeShape() {
        const {x, y, width, height} = this.props.model
        const href = this.getImageHref()
        const attrs = {
            x: x - 1 / 2 * width,
            y: y - 1 / 2 * height,
            width,
            height,
            href,
            // fit:'cover',
            // 根据宽高缩放
            preserveAspectRatio: 'none meet'
        }
        return h('g', {}, [
                h('image', {...attrs})
            ]
        );
    }

}

export default {
    type: 'image-node',
    view: ImageNode,
    model: ImageModel
}
