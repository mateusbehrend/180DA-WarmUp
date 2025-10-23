using System.Collections.Concurrent;

public class GameEngine
{
    private BlockingCollection<string> _commandQueue;
    private bool _isJumping = false;

    public GameEngine(BlockingCollection<string> commandQueue)
    {
        _commandQueue = commandQueue;
    }

    public void Run(CancellationToken token)
    {
        Console.WriteLine("GameEngine: Started. Waiting for commands...");

        try
        {
            foreach (var command in _commandQueue.GetConsumingEnumerable(token))
            {
                if (command == "JUMP" && !_isJumping)
                {
                    Task.Run(Jump);
                }
            }
        }
        catch (OperationCanceledException)
        {
            Console.WriteLine("GameEngine: Shutting down.");
        }
    }

    private async Task Jump()
    {
        _isJumping = true;
        Console.WriteLine(">>> GAME: JUMPING!");

        await Task.Delay(1000); 
        
        _isJumping = false;
        Console.WriteLine(">>> GAME: Landed.");
    }
}