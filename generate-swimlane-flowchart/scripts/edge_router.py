class EdgeRouter:


    def __init__(self):

        # 节点避让距离
        self.padding = 40



    # ==========================
    # 判断线是否经过节点
    # ==========================

    def check_collision(
            self,
            x1,
            y1,
            x2,
            y2,
            node
    ):


        nx = node["x"]
        ny = node["y"]


        # 默认节点尺寸
        nw = node.get(
            "w",
            140
        )

        nh = node.get(
            "h",
            60
        )



        left = nx - self.padding

        right = nx + nw + self.padding

        top = ny - self.padding

        bottom = ny + nh + self.padding




        # 水平线检测

        if y1 == y2:


            if top <= y1 <= bottom:


                if (
                    min(x1,x2) <= right
                    and
                    max(x1,x2) >= left
                ):

                    return True





        # 垂直线检测

        if x1 == x2:


            if left <= x1 <= right:


                if (
                    min(y1,y2) <= bottom
                    and
                    max(y1,y2) >= top
                ):

                    return True



        return False






    # ==========================
    # 自动绕线
    # ==========================

    def route(
            self,
            edge,
            layout
    ):


        source = layout[
            edge["source"]
        ]


        target = layout[
            edge["target"]
        ]



        x1 = source["x"] + 70

        y1 = source["y"] + 30



        x2 = target["x"] + 70

        y2 = target["y"] + 30




        for node_id,node in layout.items():


            # 跳过起点终点

            if node_id in [

                edge["source"],

                edge["target"]

            ]:

                continue





            if self.check_collision(

                    x1,
                    y1,
                    x2,
                    y2,
                    node

            ):



                # 从节点右侧绕行

                route_x = (

                    node["x"]

                    +

                    node.get(
                        "w",
                        140
                    )

                    +

                    self.padding

                )



                return [

                    {

                        "x":route_x,

                        "y":y1

                    },


                    {

                        "x":route_x,

                        "y":y2

                    }

                ]





        return []