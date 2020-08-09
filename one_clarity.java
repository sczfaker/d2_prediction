public class AllChatProcessor {
    @OnMessage(S2UserMessages.CUserMessageSayText2.class)
    public void onMessage(Context ctx, S2UserMessages.CUserMessageSayText2 message) {
        System.out.format("%s: %s\n", message.getParam1(), message.getParam2());
    }
    public static void main(String[] args) throws Exception {
        // 1) create an input source from the replay
        Source source = new MappedFileSource("replay.dem");
        // 2) create a simple runner that will read the replay once
        SimpleRunner runner = new SimpleRunner(source);
        // 3) create an instance of your processor
        AllChatProcessor processor = new AllChatProcessor();
        // 4) and hand it over to the runner
        runner.runWith(processor);
    }
}