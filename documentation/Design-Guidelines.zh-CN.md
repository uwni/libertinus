<!--
<style>
    img {
         margin-right: 25px;
         float: left;
         border-radius: 10px;
         box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.2), 0 6px 20px 0 rgba(0, 0, 0, 0.19);
       }
</style>
-->

# Libertinus 设计指南

这些是为所有热爱自由字体、特别是 Libertinus 字体家族并考虑为其做出贡献的志愿者准备的简短指南。
任何字体都包含大量字形。以 Libertinus 为例，它拥有数千个字形；每一个都独特，同时它们还必须彼此协调一致。字形必须在设计、视觉重量和字距上相互契合。要实现这一点，还需要处理若干技术问题。
听起来复杂？别担心，这份指南就是为了帮助你上手！

## 设计原则

每个字母的形状都是一种社会约定，通常非常古老。比如，拉丁字母源自罗马字母，罗马字母又基于希腊字母，而希腊字母则可追溯到腓尼基文字。公元 765 年，[加洛林小写](https://en.wikipedia.org/wiki/Carolingian_minuscule)被确立为书写标准，从而赋予了我们小写字母如今的形状。到了今天，借助 [Unicode](http://www.unicode.org) 我们拥有一份规范（即计算机行业标准），为世界上几乎所有已知字形定义了名称、基本形式和编码位置。

因此，字体设计师在一个框架内工作。他们需要把握字母的本质，并针对如下设计特征做出决定：

1. 衬线（Serifs）：脚部衬线、头部衬线与上升部位衬线的形态与长度，或干脆无衬线（sans-serif）；
2. 字重（Font-weight）：由笔画粗细与字距共同决定；
3. 间距/字距（Spacing / tracking）：字母之间以及字内的白区——也即内白（counter）的大小；
4. 粗细对比（Contrast）：细线与主干之间的对比；
5. 笔势/轴线（Stress/axis）：书写性的倾斜角度；
6. 比例（Proportion）：x 高度与大写高度，上伸部和下伸部的长度。

### 不完美的完美

数学上理想的形状是完美的，但往往乏味。另一方面，排版必须考虑视觉光学效应与人类视觉的特殊性。比如，圆形字符的[超出（overshoot）](https://en.wikipedia.org/wiki/Overshoot_%28typography%29)、内凹衬线（cupped serif）、渐细主干、字偶距（kerning）等，都是改善整体观感与可读性的措施。上述措施常被归为[微排版（microtypography）](https://en.wikipedia.org/wiki/Microtypography)。随着数字化，另一个特性愈发重要：相似字形的可区分性。
一个反例是 1927 年 Paul Renner 设计的著名字体 [Futura](https://en.wikipedia.org/wiki/Futura_%28typeface%29)。受包豪斯理念影响，他将字体简化为几何要素。在该字体中，`d`、`p`、`b`、`q` 是相互翻转或旋转的圆与主干；`a` 则是没有上伸部的 `d`。这种风格极度简化，同时不乏优雅，适合较大字号的展示用途，但用于正文阅读会令人吃力。当然，你也会遇到否认这一点的人——通常他们也相信“花哨”的衬线体已过时，而无衬线才是至高无上。

### Libertinus 的字重与样式

![Libertinus 字体家族的不同样式](figures/styles.png)

目前，Libertinus 提供六种样式：

- Regular 与 Italic 为标准字重（也称 “book”），以 11pt 为设计目标；
- Bold 与 Bold Italic 是上述样式的加粗版本；
- Display 是用于标题与抬头的特殊轻盈优雅变体；
- 每种样式均包含一部分小型大写（small caps）；Small Caps 样式是 Regular 的扩展小型大写集合。

### Libertinus 的衬线

![如 `n`、`m`、`r` 等字母的脚部衬线](figures/footserif.png)
#### 脚部衬线（Foot serifs）

上图展示了 Libertinus 的脚部衬线。脚部衬线最为常见，为小写 `f`、`h`、`i`、`k`、`l`、`m`、`n`、`r` 等众多字母，以及许多大写字母定型。在 `k`、`v`、`w`、`x`、`y` 等字母中，它们以对角形式出现；不仅在基线处，也在 x 高度处。在 `p` 与 `q` 中，它们构成下伸部。
图中可见，常规（Regular）与粗体（Bold）样式下衬线的厚度几乎相同，即 33 EM 与 34 EM（关于单位 “EM” 的解释见[垂直度量](#垂直度量)），而粗体样式中的主干则厚约 1.6 倍。
小提示：所示衬线的右半部分略短于左半部分，因为它是 `n` 的左侧衬线。这是为了避免脚部衬线在开口内白处过于靠近而显得狭窄，从而提高 `n` 的可读性。
小提示：衬线的左右外端略向下拱，使整体呈轻微凹形（concave），这就是所谓的“内凹衬线（cupped serif）”。

![`n` 的头部衬线](figures/headserif.png)

#### 中部头衬线（位于 x 高度）

该图展示了 `n`、`m`、`r`、`p` 的头部衬线。Libertinus 的一大特征在于：这一衬线向左弯曲，打开主干与细线连接处的夹角。
看看 `i` 与 `j`：它们的头部衬线是直立的，并未向左弯曲，因为那里的连接并不存在类似的夹角需要“打开”。
小提示：头部衬线的上方样条略呈凹形，与脚部衬线一样是“内凹”的。

![`l` 的上升部位衬线](figures/ascenderserif.png)

#### 上伸部衬线（Ascender serifs，位于上伸高度）

上伸部（或称“上部头衬线”）出现在 `b`、`d`、`h`、`k`、`l` 中。它们与 `i`、`j` 的衬线相似，但并不完全相同。

![`s` 的半衬线](figures/halfserif.png)

#### 半衬线（Half serifs）

半衬线出现在小写 `s`、`z` 以及大写 `C`、`G`、`F`、`L`、`S`、`T`、`Z` 等字母中。`s` 的半衬线几乎是垂直的，而大多数其他半衬线是斜向的。在外轮廓过渡到衬线的位置处存在直角——这是 Libertinus 的又一特征。将 `C`、`G` 等圆形字母与 `F`、`T` 等矩形字母对比观察更明显。
在粗体样式中，对角笔画会加粗，但不及竖直主干的增长幅度。这是因为内白（counter）会变小，字形自身的视觉重量已随之增加。
小提示：半衬线的形态并非内凹，甚至略带外凸（convex）。

![`f` 右侧钩端的水滴形收笔](figures/dropterminals.png)

#### 水滴形收笔（Drop terminals）

水滴形收笔出现在 `a`、`c`、`f`、`g`、`j`、`r`、`y` 等字母中。
在粗体样式中，水滴显著加重，而细线并未同步大幅增粗。图中还可看到，粗体的 x 高度较常规体提升了约 5 EM。
小提示：Libertinus 的水滴末端是扁平化处理的。同时你会注意到句点 `.`、逗号 `,` 与引号 `"` 的圆点也被压扁，这是 Libertinus 的又一特征。

### 两个首要设计母版 …

开发一款字体时，通常从极少量的字母（或“字形”）起步，并将其定义为设计母版。在 Libertinus 中，它们是 `n` 与 `o`。
反过来讲，若修改它们便会与大量派生字母发生冲突，所以最好不要轻易改动。

![`n` 作为设计母版](figures/n-Referenzglyph.png)

#### … 带衬线的字母以 `n` 为母版
小写字母 `n` 确定：

- 衬线的形式；
- 主干宽度：小写为 79 EM，由此推导大写为 85 EM；
- 间距：两条主干之间的内部距离。内白的大小会影响字距；它被视为字母之间光学间距的默认参照；
- 字重：由主干宽度和字距共同作用；
- x 高度与超出（overshoot）：小写字母的主体高度为 429 EM。圆形部件在 x 高度线与基线之上/之下约超出 10 EM。这一排版措施使 `o`、`e`、`c` 以及 `n`、`m`、`r` 等与 `x` 的“视觉高度”一致。在 FontForge 中，超出走廊以玫瑰色标示。

派生字母：`m`、`r`、`h`、`i`、`j`、`l`、`u` …

![`o` 作为设计母版、笔势角度与光学边承](figures/o-Referenzglyph.png)
#### … 含圆部件的字母以 `o` 为母版
小写字母 `o` 为所有含圆部件的字母确定如下特征：

- 笔势（stress）：书写性的倾斜角度；
- 圆笔画的最小/最大宽度：最细为 35 EM，最粗为 86 EM；
- 间距：内白大小影响字距。理由是字形之间的白区（左右光学边承之和）应与内白大致相当。为字形找准恰当的间距是一项艰难工作；
- 边承（bearings）：作为圆形字母间距的指示。

图右显示了一个粗体 `o`，其上叠放着常规体 `o` 的尖锐轮廓。可见竖直笔画变粗，而细线几乎不变。字形主要在外侧加重并变宽；同时内侧也会加粗，从而使内白缩小。笔画加粗与内白缩小共同提升了字重。

派生字母：`e`、`c`，以及 `b`、`d`、`p`、`q`、`g` 等字母的圆部件。注意：“派生”并不意味着简单的复制粘贴。涉及圆部件时，你总需要对形态、重量与边承做出调整与优化。

### 次要设计母版

除了 `n` 与 `o`，所有基础字母也构成次要设计母版集合。下表列出这些次要设计母版的 Unicode 范围。

| 字母集            | 字形                 | Unicode 范围 | 图表                                        |
|:------------------|:---------------------|:-------------|:--------------------------------------------|
| 基本拉丁（ASCII） | `0--9` `A--Z` `a--z` | 0000--007F   | [PDF](figures/LF-Libertinus_BasicLatin.pdf) |
| 基本希腊文        | `Α--Ω` `α--ω`        | 0370--03FF   | [PDF](figures/LF-Libertinus_BasicGreek.pdf) |
| 基本西里尔文      | `А--Я` `а--я`        | 0400--04FF   | 待办                                        |

### 垂直度量

![高度与超出边距](figures/heights.png)

上图展示了 Libertinus Regular 的垂直度量。水平边线被称为“高度（heights）”。例如，**x 高度**是 `a`、`c`、`e` … `x` 等小写字母主体的上边界。Libertinus 的大写高度（caps-height）略低于小写字母的上伸高度（ascender-height）。数字也有各自的**数字高度（numbers-height）**；小型大写有各自的**大写高度（caps-height）**。
按定义，EM 方框的高度被分为 1000 个单位，称为 “EM 单位” 或简称 “EM”。简而言之，我们在一个笛卡尔坐标系中工作。
小提示：玫瑰色的边距即为“超出边距（overshoot margins）”。如前所述，圆形部件需要超出基线/高度线，以形成视觉上的齐整。

### 间距与字距（Spacing and tracking）

![字距需要基于光学评估，并与内白相协调](figures/spacing.png)

当你画好了一个漂亮的字形，工作并没有结束。为字形设定合适的间距与字距是核心任务之一。你需要检查几十种字偶组合，并在其中做许多权衡。图中蓝色表示内白，红色表示字形之间的间距。内白在字距中扮演重要角色；二者应当达到均衡。
回想那张展示粗体 `o` 的图：更细的内白会导致更紧的字距，从而使字面密度更高、字重更重。
Libertinus 的字形已具备相当不错的基础间距。如果你要为新字形设定间距或改进现有间距，请选取一个与你相似的参考字形，再据此作出判断。

### 超出与高度度量（Overshoot and height metrics）

请补充说明。

## FontForge 字体编辑器

![FontForge 的字视图](figures/fontforge-fontview.png)

Libertinus 使用 FontForge 字体编辑器进行开发。多数 Linux 发行版（Ubuntu、Fedora、OpenSUSE …）、macOS 与 Windows 都有二进制安装包。更多信息见 [FontForge 项目页](http://fontforge.github.io)。
另有相当不错的手册可供参考：[Design fonts with FontForge](http://designwithfontforge.com/en-US/index.html)。

### 图层（Layers）

在字形视图中，你会看到一个名为“图层”的小工具箱。Libertinus 的轮廓存放在“字形图层（glyph layer）”。你可以使用“背景图层（background layer）”存放来自其他字形的轮廓，用于比较形态、高度、内白宽度等特征。最后，“参考线图层（guide layer）”包含 x 高度、大写高度等度量线，并在所有字形间共享。因此，请不要改动该图层。

### 绘制样条与轮廓（Drawing splines and contours）

![四种点类型与轮廓绘制](figures/r-Point-types.png)

TTF 与 OTF 等矢量字体使用[贝塞尔曲线](https://en.wikipedia.org/wiki/B%C3%A9zier_curve)。你也许在 Inkscape 或 Illustrator 等矢量图编辑器中见过。FontForge 提供四种点类型：

1. 曲线点（curve point）：左右手柄联动；
2. 水平/垂直曲线点（h/v curve point）：手柄严格水平或垂直；
3. 拐角点（corner point）：左右手柄相互独立；
4. 切线点（tangent point）：手柄沿入射样条方向延伸。

你可以通过点菜单轻松更改点类型。右键点击某个点会打开上下文菜单，以便精确控制点与其手柄的位置与类型。

轮廓必须闭合，只有闭合轮廓才会填充。外轮廓需按顺时针标记；内轮廓（构成内白）需按逆时针标记。

### 重音字形（Accented glyphs）

#### 使用引用（references）

![引用与 Use my metrics 选项用法](figures/i-Referenzglyph-UseMyMetrics.png)

拉丁编码页包含大量的重音字符。它们通常只是基本字形与重音符号的不同组合。例如，`é` 由 `e` + `´` 组合而成。在这些情况下，你不必复制轮廓；完全可以、而且应该使用指向原始字形的“引用”。

示例：字母 `i` 实际上也是一个重音字符，由 `ı`（名为 dotlessi）与 `˙`（名为 dotaccent）组合而成。为确保被引用字形在度量上的改进能传递至派生字形，需要勾选“Use my metrics”（使用我的度量）。
几乎所有可以想象的重音符号如今都已编码。你可以在以下两张 Unicode 图表中找到它们：
- [Unicode-Chart Combining Diacritical Marks U+0300--U+036F](http://unicode.org/charts/PDF/U0300.pdf)
- [Supplement U+1DC0--U+1DFF](http://unicode.org/charts/PDF/U1DC0.pdf)

#### 基底标记与锚点（Base marks and anchors）

请补充说明。

## 作者（Authors）

- Gillian Tiefenlicht [GillianTL](https://github.com/GillianTL)
