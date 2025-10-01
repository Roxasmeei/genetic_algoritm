

class DPSolver:
    def __init__(self, constraints, weights, costs, max_weight):
        self.constraints = constraints
        self.weights = weights
        self.costs = costs
        self.max_weight = max_weight

    def solve(self):
        n = len(self.weights)
        occupied_weight = sum([self.weights[i] * self.constraints[i] for i in range(n)])
        
        W = self.max_weight - occupied_weight

        # dp[w] = максимальная стоимость для веса w
        dp = [0 for _ in range(W + 1)]

        # Заполняем таблицу DP
        for w in range(1, W + 1):
            for i in range(n):
                if self.weights[i] <= w:
                    dp[w] = max(dp[w], dp[w - self.weights[i]] + self.costs[i])

        # Восстанавливаем решение
        quantities = [0] * n
        w = W
        while w > 0:
            best_item = -1
            best_value = 0
            for i in range(n):
                if self.weights[i] <= w:
                    value = dp[w - self.weights[i]] + self.costs[i]
                    if value > best_value:
                        best_value = value
                        best_item = i

            if best_item == -1:
                break

            quantities[best_item] += 1
            w -= self.weights[best_item]

        return dp[W] + sum(self.constraints[i] * self.costs[i] for i in range(n)), [quantities[i] + self.constraints[i] for i in range(n)]