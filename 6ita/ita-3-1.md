3. 深度学习的数学基础
3.1 高等数学基础

### 函数的定义
- 量和量之间的关系如: $ A = \pi r^2 $
- $ y = f(x) $ 其中 $ x $ 是自变量, $ y $ 是因变量
- 函数在 $ x\_0 $ 处取得的函数值 $ y\_0 = \left. y \right|\_{x = x\_0} = f(x\_0) $
- 符号只是一种表示, 也可以: $ y = g(x) $, $ y = \varphi(y) $, $ y = \psi(x) $

### 几种函数
- 分段函数
- 反函数
- 显函数与隐函数

### 分段函数
$$
f(x) = \begin{cases}
\sqrt{x}, & x \geq 0 \\\
-x, & x < 0
\end{cases}
$$

### 反函数
- 若 $ y = f(x) $, 则反函数表示为 $ x = f^{-1}(y) $
$$
h = \frac{1}{2} g t^2 \rightarrow h = h(t)
$$
$$
t = \sqrt{\frac{2h}{g}} \rightarrow t = t(h)
$$

### 显函数与隐函数
- 显函数形式如 $ y = f(x) $
$$
y = x^2 + 1
$$
- 隐函数形式如 $ F(x, y) = 0 $
$$
3x + y - 4 = 0
$$

### 函数的几种特性
- 奇偶性
- 周期性
- 单调性

### 奇偶性
- 偶函数: y 轴对称
$$
f(-x) = f(x)
$$
$$
f(x)= x^2
$$
$$f(-x) = (-x)^2 = x^2 = f(x)
$$
- 奇函数: 原点对称
$$
f(-x) = - f(x)
$$
$$
f(x)= x^3
$$
$$
f(-x) = (-x)^3 = -x^3 = - f(x)
$$

### 周期性
$$
f(x+T) = f(x)
$$

### 单调性
- 单调递增函数
$$
f(x) = \log(x+1)
$$
- 单调递减函数
$$
f(x) = -\log(x+1)
$$

### 数列
- 按照一定次序排列的一列数 $ u\_1, u\_2, \cdots, u\_n, \cdots $ 其中 $ u_n $ 叫做通项
- 对于数列 $ \\{ u\_n \\} $ :
- 如果当 $ n $ 无限增大时, 其通项无限接近于一个常数 $ A $
- 则称该数列以 $ A $ 为极限, 或数列收敛于 $ A $
- $ \lim\limits\_{n \to \infty} u\_n = A, $ 或 $ u\_n \to A \ (n \to \infty) $
- 否则称数列为发散
- $ \lim\limits\_{n \to \infty} \frac{1}{3^n} = 0, \quad \lim\limits\_{n \to \infty} \frac{n}{n+1} = 1, \quad \lim\limits\_{n \to \infty} 2^n $ 不存在

### 符号表示
- $ x \to \infty $ 表示 "当 $ |x| $ 无限增大时"
- $ x \to +\infty $ 表示 "当 $ x $ 无限增大时"
- $ x \to -\infty $ 表示 "当 $ x $ 无限减小时"
- $ x \to x\_0 $ 表示 "当 $ x $ 从 $ x\_0 $ 左右两侧无限接近 $ x\_0 $ 时"
- $ x \to x\_0^+ $ 表示 "当 $ x $ 从 $ x\_0 $ 右侧无限接近 $ x\_0 $ 时"
- $ x \to x\_0^- $ 表示 "当 $ x $ 从 $ x\_0 $ 左侧无限接近 $ x\_0 $ 时"

### 极限
$$ \lim\limits\_{x \to +\infty} e^{-x} = 0 $$
$$ \lim\limits\_{x \to \infty} \frac{1}{x} = 0 $$
$$ \lim\limits\_{x \to -\infty} \arctan{x} = -\frac{\pi}{2} $$

### 极限
- 函数在 $ x\_0 $ 的领域内有定义, $ \lim\limits\_{x \to x\_0} f(x) = A, $ 或 $ f(x) \to A \ (x \to x\_0) $
$$
\lim\limits\_{x \to 1} \frac{x^2 - 1}{x - 1} = \lim\limits\_{x \to 1} \frac{(x-1)(x+1)}{x-1} = 2
$$
- 左右极限: 函数在左半领域/右半领域内有定义
- $ \lim\limits\_{x \to x\_0^+} f(x) = A $, 或 $ f(x) \to A \ (x \to x\_0^+) $
- $ \lim\limits\_{x \to x\_0^-} f(x) = A $, 或 $ f(x) \to A \ (x \to x\_0^-) $

### 极限
- $ \lim\limits\_{x \to x\_0} f(x) = A $ 的充要条件是
$$ \lim\limits\_{x \to x\_0^-} f(x) = \lim\limits_{x \to x\_0^+} f(x) = A $$

### 极限
$$ f(x) = \begin{cases}
x - 1, & x < 0 \\\
0, & x = 0 \\\
x + 1, & x > 0
\end{cases} $$
 当 $ x \to 0 $ 时 $ f(x) $ 的极限
$$ \lim\limits\_{x \to 0^+} f(x) = \lim\limits\_{x \to 0^+} (x + 1) = 1 $$
$$ \lim\limits\_{x \to 0^-} f(x) = \lim\limits\_{x \to 0^-} (x - 1) = -1 $$
$ \therefore \lim\limits\_{x \to 0} f(x) $ 不存在

### 极限
- 无穷小: 以零为极限
  $ \lim\limits\_{x \to \infty} \frac{1}{x} = 0 $, 则 $ \frac{1}{x} $ 是 $ x \to \infty $ 时的无穷小
  $ \lim\limits\_{x \to 2} (3x - 6) = 0 $, 则 $ 3x - 6 $ 是 $ x \to 2 $ 的无穷小

- 基本性质:
  - 有限个无穷小的代数和仍然是无穷小
  - 有限个无穷小的积仍然是无穷小
  - 有界变量与无穷小的积仍然是无穷小
  - 无限个无穷小之和不一定是无穷小

$$ \lim\limits\_{n \to \infty} \left( \frac{1}{n^2} + \frac{2}{n^2} + \cdots + \frac{n}{n^2} \right) = \lim\limits\_{n \to \infty} \frac{n(n+1)}{2n^2} = \lim\limits\_{n \to \infty} \frac{n+1}{2n} = \frac{1}{2} $$

### 极限
- 无穷小的商不一定是无穷小
  $ \lim\limits\_{x \to 0} \frac{x}{2x} = \frac{1}{2} $, $ \lim\limits\_{x \to 0} \frac{x^2}{2x} = 0 $, $ \lim\limits\_{x \to 0} \frac{2x}{x^2} = \infty $

- 极限有无穷小的关系:
  $ \lim\limits\_{x \to x\\_0} f(x) = A $ 的充要条件 $ f(x) = A + \alpha(x) $, 其中 $ \alpha(x) $ 是 $ x \to x\\_0 $ 时的无穷小

### 极限
- 无穷大: 并不是一个很大的数, 是相对于变换过程来说
  $$ \lim\limits\_{x \to x\\_0} f(x) = \infty $$ 或 $ f(x) \to \infty \ (x \to x\\_0) $

- 无穷小和无穷大的关系: 在自变量的变换的同一过程中, 如果 $ f(x) $ 为无穷大, 那么 $ \frac{1}{f(x)} $ 为无穷小

### 极限
- 无穷小的比较: $\alpha = \alpha(x)$, $\beta = \beta(x)$ 都是无穷小
  $$ \lim\limits\_{x \to x\\_0} \alpha(x) = 0, \lim\limits\_{x \to x\\_0} \beta(x) = 0 $$

- 如果 $ \lim\limits\_{x \to x\\_0} \frac{\beta}{\alpha} = 0 $, 则称 $\beta$ 是比 $\alpha$ 高阶无穷小
- 如果 $ \lim\limits\_{x \to x\\_0} \frac{\beta}{\alpha} = \infty $, 则称 $\beta$ 是比 $\alpha$ 低阶无穷小
- 如果 $ \lim\limits\_{x \to x\\_0} \frac{\beta}{\alpha} = C \neq 0 $, 则称 $\beta$ 与 $\alpha$ 是同阶无穷小

### 函数的连续性
- 设函数 $ y = f(x) $ 在点 $ x\_0 $ 的某邻域内有定义, 如果当自变量的改变量 $ \Delta x $ 趋近于零时, 相应函数的改变量 $ \Delta y $ 也趋近于零, 则称 $ y = f(x) $ 在点 $ x\_0 $ 处连续
  $$ \lim\limits\_{\Delta x \to 0} \Delta y = \lim\limits\_{\Delta x \to 0} \left[ f(x\_0 + \Delta x) - f(x\_0) \right] = 0 $$

### 函数的连续性
- 函数 $ f(x) $ 在点 $ x\_0 $ 处连续, 需要满足的条件:
  1. 函数在该点处有定义
  2. 函数在该点处极限 $ \lim\limits\_{x \to x\_0} f(x) $ 存在
  3. 极限值等于函数值 $ f(x\_0) $

### 函数的连续性
- 函数 $ f(x) = \begin{cases} x+1 & x \leq 0 \\ \frac{\sin x}{x} & x > 0 \end{cases} $ 在 $ x = 0 $ 处的连续性？

- $ f(0) = 1 $
  $$ \lim\limits\_{x \to 0^-} f(x) = \lim\limits\_{x \to 0^-} (x+1) = 1 $$
  $$ \lim\limits\_{x \to 0^+} f(x) = \lim\limits\_{x \to 0^+} \frac{\sin x}{x} = 1 $$
  $$ \lim\limits\_{x \to 0} f(x) = f(0) = 1 $$

### 函数的间断点
- 函数 $ f(x) $ 在点 $ x = x\_0 $ 处不连续, 则称其为函数的间断点

- 3 种情况为间断点:
  1. 函数 $ f(x) $ 在点 $ x\_0 $ 处没有定义
  2. 极限 $ \lim\limits\_{x \to x\_0} f(x) $ 不存在
  3. 满足前两点, 但是 $ \lim\limits\_{x \to x\_0} f(x) \neq f(x\_0) $

### 函数的间断点
- 当 $ x \to x\_0 $ 时, $ f(x) $ 的左右极限存在, 则称 $ x\_0 $ 为 $ f(x) $ 的第一类间断点, 否则为第二类间断点

- 跳跃间断点: 
  $$ \lim\limits\_{x \to 0^-} f(x) $$ 与 $$ \lim\limits\_{x \to 0^+} f(x) $$ 均存在, 但不相等

- 可去间断点: 
  $$ \lim\limits\_{x \to x\_0} f(x) $$ 存在但不等于 $ f(x\_0) $

### 函数的间断点
- 函数 $ f(x) = \frac{x^2 - 1}{x^2 - 3x + 2} $ 的连续型？

- 在点 $ x = 2 $, $ x = 1 $ 处没有定义

  $$ \lim\limits\_{x \to 1^-} \frac{x^2 - 1}{x^2 - 3x + 2} = \lim\limits\_{x \to 1^-} \frac{x + 1}{x - 2} = -2 $$

  $$ \lim\limits\_{x \to 1^+} \frac{x^2 - 1}{x^2 - 3x + 2} = \lim\limits\_{x \to 1^+} \frac{x + 1}{x - 2} = -2 $$

- 在 $ x = 1 $ 处是可去间断点

  $$ \lim\limits\_{x \to 2^-} f(x) = -\infty $$

  $$ \lim\limits\_{x \to 2^+} f(x) = +\infty $$

- 在 $ x = 2 $ 处是第二类间断点

### 导数
- 平均速度: (速度) $ \bar{\nu} = \frac{s(路程)}{t(时间)} $ 但是如何表示瞬时速度呢？

- 瞬时经过路程: $ \Delta s = s(t\_0 + \Delta t) - s(t\_0) $

- 这一小段的平均速度: $ \bar{\nu} = \frac{\Delta s}{\Delta t} = \frac{s(t\_0 + \Delta t) - s(t\_0)}{\Delta t} $

- 当 $ \Delta t \to 0 $ 时也就是瞬时速度了
  $$ \nu(t\_0) = \lim\limits\_{\Delta t \to 0} \bar{\nu} = \lim\limits\_{\Delta t \to 0} \frac{\Delta s}{\Delta t} = \lim\limits\_{\Delta t \to 0} \frac{s(t\_0 + \Delta t) - s(t\_0)}{\Delta t} $$

### 导数
- 如果平均变化率的极限存在,
  $$ \lim\limits\_{\Delta x \to 0} \frac{\Delta y}{\Delta x} = \lim\limits\_{\Delta x \to 0} \frac{f(x\_0 + \Delta x) - f(x\_0)}{\Delta x} $$

  则称此极限为函数 $ y = f(x) $ 在点 $ x\_0 $ 处的导数, $ f'(x\_0) $

  $$ y' \Big|\_{x = x\_0} \quad 或 \quad \frac{dy}{dx} \Big|\_{x = x\_0} \quad 或 \quad \frac{df(x)}{dx} \Big|\_{x = x\_0} $$

### 导数
1. $ (C)' = 0 $
2. $ (x^\mu)' = \mu \cdot x^{\mu - 1} $
3. $ (\sin x)' = \cos x $
4. $ (\cos x)' = -\sin x $
5. $ (\tan x)' = \sec^2 x $
6. $ (\cot x)' = -\csc^2 x $
7. $ (\sec x)' = \sec x \cdot \tan x $
8. $ (\csc x)' = -\csc x \cdot \cot x $
9. $ (a^x)' = a^x \cdot \ln a $
10. $ (e^x)' = e^x $
11. $ (\log\_a x)' = \frac{1}{x \ln a} $
12. $ (\ln x)' = \frac{1}{x} $
13. $ (\arcsin x)' = \frac{1}{\sqrt{1 - x^2}} $
14. $ (\arccos x)' = -\frac{1}{\sqrt{1 - x^2}} $
15. $ (\arctan x)' = \frac{1}{1 + x^2} $
16. $ (\text{arccot} x)' = -\frac{1}{1 + x^2} $

### 导数
1. $ (u \pm v)' = u' \pm v' $
2. $ (uv)' = u'v + uv' $
3. $ \left( \frac{u}{v} \right)' = \frac{u'v - uv'}{v^2} \quad (v \neq 0) $
4. $ (Cu)' = Cu' $
5. $ \left( \frac{C}{v} \right)' = \frac{-Cv'}{v^2} \quad (C \text{为常数}) $


