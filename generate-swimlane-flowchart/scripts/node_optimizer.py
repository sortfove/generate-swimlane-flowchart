class NodeOptimizer:


    def __init__(self):

        # 节点尺寸
        self.node_width = 140
        self.node_height = 60

        # 自动下移距离
        self.move_distance = 120



    # ==========================
    # 判断垂直连线是否穿过节点
    # ==========================

    def block_vertical_edge(
            self,
            source,
            target,
            node
    ):


        # 判断是否同一条竖线

        source_x = source["x"] + self.node_width / 2

        target_x = target["x"] + self.node_width / 2



        if abs(source_x-target_x) > 10:

            return False



        node_left = node["x"]

        node_right = (
            node["x"]
            +
            self.node_width
        )


        node_top = node["y"]

        node_bottom = (
            node["y"]
            +
            self.node_height
        )



        # x轴是否经过节点

        if not (
            node_left
            <=
            source_x
            <=
            node_right
        ):

            return False



        # y范围是否重叠

        edge_top = min(
            source["y"],
            target["y"]
        )


        edge_bottom = max(
            source["y"],
            target["y"]
        )



        if (

            node_top > edge_top

            and

            node_bottom < edge_bottom

        ):

            return True



        return False




    # ==========================
    # 优化节点位置
    # ==========================

    def optimize(
            self,
            layout,
            edges
    ):


        for edge in edges:


            source = layout[
                edge["source"]
            ]


            target = layout[
                edge["target"]
            ]



            for node_id,node in layout.items():


                # 跳过起点终点

                if node_id in [

                    edge["source"],

                    edge["target"]

                ]:

                    continue




                if self.block_vertical_edge(

                    source,

                    target,

                    node

                ):


                    # 向下移动

                    node["y"] += self.move_distance



        return layout