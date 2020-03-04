from .head import Head
from ..modules.convolution import Conv2dAct


class SSDLiteExtraLayers(Head):
    def __init__(self, backbone, width_multiplier=1):
        m = width_multiplier
        base_output_shapes = Head.get_base_output_shapes(backbone, [4, 5])
        output_channels = base_output_shapes + [int(512 * m), int(256 * m), int(256 * m), int(128 * m)]
        super(SSDLiteExtraLayers, self).__init__(backbone, [4, 5], output_channels)
        in_channels = base_output_shapes[-1]

        self.conv0_0 = Conv2dAct(in_channels, in_channels, kernel_size=3, padding=1, stride=2, groups=in_channels, use_bn=True)
        self.conv0_1 = Conv2dAct(in_channels, int(512 * m), kernel_size=1, use_bn=True)
        self.conv1_0 = Conv2dAct(int(512 * m), int(512 * m), kernel_size=3, padding=1, stride=2, groups=int(512 * m), use_bn=True)
        self.conv1_1 = Conv2dAct(int(512 * m), int(256 * m), kernel_size=1, use_bn=True)
        self.conv2_0 = Conv2dAct(int(256 * m), int(256 * m), kernel_size=3, padding=1, stride=2, groups=int(256 * m), use_bn=True)
        self.conv2_1 = Conv2dAct(int(256 * m), int(256 * m), kernel_size=1, use_bn=True)
        self.conv3_0 = Conv2dAct(int(256 * m), int(256 * m), kernel_size=3, padding=1, stride=2, groups=int(256 * m), use_bn=True)
        self.conv3_1 = Conv2dAct(int(256 * m), int(128 * m), kernel_size=1, use_bn=True)

    def forward(self, input):
        features = self.get_base_features(input)
        f0 = self.conv0_1(self.conv0_0(features[-1]))
        f1 = self.conv1_1(self.conv1_0(f0))
        f2 = self.conv2_1(self.conv2_0(f1))
        f3 = self.conv3_1(self.conv3_0(f2))
        return features + [f0, f1, f2, f3]